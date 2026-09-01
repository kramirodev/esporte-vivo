import asyncio
from datetime import datetime
from uuid import UUID, uuid4

from app.database import models
from app.database.redis_conexao import redis_client
from app.database.sqlalchemy_conexao import _sessionLocal
from app.services.matchmaking import (
    CHAVE_FILAS_ATIVAS,
    obter_chave_fila,
    obter_chave_mmr,
    obter_chave_usuario,
)
from app.services.mmr import avaliar_partida, peso_elo
from app.services.websocket_manager import manager

INTERVALO_WORKER_SEGUNDOS = 5
TEMPO_LOCK_SEGUNDOS = 15


def _obter_jogadores_balanceados(esporte_id: int, tamanho_time: int) -> list[tuple[str, int, str]]:
    ids = redis_client.zrange(obter_chave_fila(esporte_id), 0, -1)
    mmrs = redis_client.hmget(obter_chave_mmr(esporte_id), ids)
    jogadores = [(str(usuario_id), int(mmr or 1000)) for usuario_id, mmr in zip(ids, mmrs)]
    jogadores.sort(key=lambda jogador: jogador[1], reverse=True)
    selecionados = jogadores[:tamanho_time * 2]
    times: list[list[tuple[str, int]]] = [[], []]
    for indice, jogador in enumerate(selecionados):
        times[indice % 2].append(jogador)
    return [
        (usuario_id, mmr, 'A' if indice == 0 else 'B')
        for indice, time in enumerate(times)
        for usuario_id, mmr in time
    ]


def _tentar_formar_partida(esporte_id: int) -> dict | None:
    lock_key = f'lock:matchmaking:{esporte_id}'
    lock_token = str(uuid4())
    if not redis_client.set(lock_key, lock_token, nx=True, ex=TEMPO_LOCK_SEGUNDOS):
        return None

    db = _sessionLocal()
    try:
        esporte = db.query(models.esporte).filter(
            models.esporte.id == esporte_id,
            models.esporte.ativo.is_(True)
        ).first()
        if esporte is None:
            redis_client.srem(CHAVE_FILAS_ATIVAS, esporte_id)
            return None

        jogadores = _obter_jogadores_balanceados(esporte_id, esporte.jogadores_por_time)
        if len(jogadores) < esporte.jogadores_por_time * 2:
            return None

        pesos_a = [peso_elo(mmr) for _, mmr, time in jogadores if time == 'A']
        pesos_b = [peso_elo(mmr) for _, mmr, time in jogadores if time == 'B']
        resultado = avaliar_partida(pesos_a, pesos_b)
        if not resultado.aprovado:
            return None

        partida = models.partida(
            esporte_id=esporte_id,
            local_id=None,
            tipo='casual',
            status='formada',
            data_hora_agendada=datetime.utcnow(),
            elo_medio=round(sum(mmr for _, mmr, _ in jogadores) / len(jogadores)),
            time_vencedor='aguardando'
        )
        db.add(partida)
        db.flush()
        for usuario_id, _, time in jogadores:
            db.add(models.partida_jogador(
                partida_id=partida.id,
                usuario_id=UUID(usuario_id),
                time_alocado=time,
                compareceu=False,
                variacao_elo_obtida=0
            ))
        db.commit()

        pipeline = redis_client.pipeline()
        for usuario_id, _, _ in jogadores:
            pipeline.zrem(obter_chave_fila(esporte_id), usuario_id)
            pipeline.srem(obter_chave_usuario(UUID(usuario_id)), esporte_id)
            pipeline.hdel(obter_chave_mmr(esporte_id), usuario_id)
        pipeline.execute()
        if redis_client.zcard(obter_chave_fila(esporte_id)) == 0:
            redis_client.srem(CHAVE_FILAS_ATIVAS, esporte_id)

        return {
            'partida_id': str(partida.id),
            'esporte_id': esporte_id,
            'status': partida.status,
            'times': {
                'A': [usuario_id for usuario_id, _, time in jogadores if time == 'A'],
                'B': [usuario_id for usuario_id, _, time in jogadores if time == 'B'],
            },
            'elo_medio': partida.elo_medio,
            'quality_score': resultado.quality_score,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        if redis_client.get(lock_key) == lock_token:
            redis_client.delete(lock_key)


async def processar_filas() -> None:
    for esporte_id in redis_client.smembers(CHAVE_FILAS_ATIVAS):
        partida = await asyncio.to_thread(_tentar_formar_partida, int(esporte_id))
        if partida:
            usuarios = partida['times']['A'] + partida['times']['B']
            await manager.broadcast(usuarios, {'evento': 'partida_formada', 'partida': partida})


async def executar_worker(stop_event: asyncio.Event) -> None:
    while not stop_event.is_set():
        try:
            await processar_filas()
        except Exception:
            pass
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=INTERVALO_WORKER_SEGUNDOS)
        except asyncio.TimeoutError:
            continue