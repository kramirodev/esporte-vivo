import time
from uuid import UUID
from app.database.redis_conexao import redis_client

CHAVE_FILAS_ATIVAS = 'filas:ativas'

# --- Auxiliares ---

def obter_chave_fila(esporte_id: int) -> str:
    return f"fila:esporte:{esporte_id}"

def obter_chave_usuario(usuario_id: UUID) -> str:
    return f"usuario_filas:{usuario_id}"

def obter_chave_mmr(esporte_id: int) -> str:
    return f"fila:esporte:{esporte_id}:mmr"

# --- Operações de Fila ---

def entrar_na_fila(
    usuario_id: UUID,
    esportes_ids: list[int],
    mmr_por_esporte: dict[int, int]
) -> dict:
    chave_user = obter_chave_usuario(usuario_id)
    id_user = str(usuario_id)
    agora = time.time()

    # Busca os IDs inscritos e garante a conversão para string
    inscritos_raw = redis_client.smembers(chave_user)
    ja_inscritos = []
    for item in inscritos_raw:
        if isinstance(item, bytes):
            ja_inscritos.append(item.decode('utf-8'))
        else:
            ja_inscritos.append(str(item))

    # Filtra apenas os esportes em que ainda não está inscrito
    novos_esportes = []
    for esp_id in esportes_ids:
        if str(esp_id) not in ja_inscritos:
            novos_esportes.append(esp_id)

    if not novos_esportes:
        return {"sucesso": False, "motivo": "Usuário já está em todas as filas selecionadas."}

    pipe = redis_client.pipeline()
    for esp_id in novos_esportes:
        pipe.zadd(obter_chave_fila(esp_id), {id_user: agora})
        pipe.sadd(chave_user, esp_id)
        pipe.hset(obter_chave_mmr(esp_id), id_user, mmr_por_esporte[esp_id])
        pipe.sadd(CHAVE_FILAS_ATIVAS, esp_id)
    pipe.execute()

    return {"sucesso": True, "esportes_adicionados": novos_esportes}


def sair_da_fila(usuario_id: UUID, esporte_id: int | None = None) -> dict:
    chave_user = obter_chave_usuario(usuario_id)
    id_user = str(usuario_id)

    esportes_remover = []

    if esporte_id is not None:
        esportes_remover.append(esporte_id)
    else:
        esportes_no_redis = redis_client.smembers(chave_user)
        for esp in esportes_no_redis:
            esportes_remover.append(int(esp))

    if not esportes_remover:
        return {"sucesso": False, "motivo": "Usuário não está em nenhuma fila."}

    pipe = redis_client.pipeline()
    for esp_id in esportes_remover:
        pipe.zrem(obter_chave_fila(esp_id), id_user)
        pipe.srem(chave_user, esp_id)
        pipe.hdel(obter_chave_mmr(esp_id), id_user)
    pipe.execute()

    for esp_id in esportes_remover:
        if redis_client.zcard(obter_chave_fila(esp_id)) == 0:
            redis_client.srem(CHAVE_FILAS_ATIVAS, esp_id)

    return {"sucesso": True, "esportes_removidos": esportes_remover}


def consultar_status_usuario(usuario_id: UUID) -> dict:
    chave_user = obter_chave_usuario(usuario_id)
    id_user = str(usuario_id)
    esportes = redis_client.smembers(chave_user)

    if not esportes:
        return {"em_fila": False, "filas_ativas": []}

    agora = time.time()
    filas_detalhes = []

    for esp_id_str in esportes:
        esp_id = int(esp_id_str)
        chave_fila = obter_chave_fila(esp_id)

        score = redis_client.zscore(chave_fila, id_user)
        total = redis_client.zcard(chave_fila)

        tempo_espera = 0
        if score:
            tempo_espera = int(agora - float(score))

        filas_detalhes.append({
            "esporte_id": esp_id,
            "tempo_espera_segundos": tempo_espera,
            "total_jogadores_na_fila": total
        })

    return {
        "em_fila": True,
        "total_filas_ativas": len(filas_detalhes),
        "filas_ativas": filas_detalhes
    }