import random
from datetime import time
from sqlalchemy import func
from app.database.sqlalchemy_conexao import _sessionLocal
from app.database import models

def popular_banco_para_testes():
    db = _sessionLocal()
    
    esporte = db.query(models.esportes).filter(models.esportes.nome == "Futebol").first()
    if not esporte:
        esporte = models.esportes(
            nome="Futebol",
            jogadores_por_time=5,
            ativo=True
        )
        db.add(esporte)
        db.commit()
        db.refresh(esporte)
        print(f"Esporte criado: Futebol (ID: {esporte.id})")

    esporte_id_teste = esporte.id
    dia_teste = 6  # Domingo
    
    print("Criando 30 jogadores de teste...")

    for i in range(1, 31):
        # Gera coordenadas próximas
        lat = -22.90 + random.uniform(-0.05, 0.05)
        lon = -43.20 + random.uniform(-0.05, 0.05)
        
        ponto_wkt = f"POINT({lon} {lat})"
        geom = func.ST_GeomFromText(ponto_wkt, 4326)
        
        # 2. Cria o Usuário Falso
        novo_usuario = models.usuario(
            telefone=f"2199999{i:04d}",
            nome=f"Jogador Teste {i}",
            apelido=f"Jg{i}",
            geom_localizacao=geom,
            trust_factor=60 + i,
            status_conta="ativo",
            is_premium=False
        )
        db.add(novo_usuario)
        db.commit() 
        db.refresh(novo_usuario)
        
        # 3. Cria o Elo e Histórico consistente
        elo_aleatorio = random.randint(800, 2200)
        partidas_jogadas = random.randint(6, 25)
        partidas_vencidas = random.randint(0, partidas_jogadas)
        partidas_empates = random.randint(0, partidas_jogadas - partidas_vencidas)
        partidas_perdidas = partidas_jogadas - partidas_vencidas - partidas_empates

        novo_elo = models.usuario_elo(
            usuario_id=novo_usuario.id,
            esporte_id=esporte_id_teste,
            pontuacao_elo=elo_aleatorio,
            partidas_jogadas=partidas_jogadas,
            vitorias=partidas_vencidas,
            derrotas=partidas_perdidas,
            empates=partidas_empates
        )
        db.add(novo_elo)
        
        # 4. Cria a Disponibilidade Padrão
        nova_disp = models.disponibilidade_padrao(
            usuario_id=novo_usuario.id,
            esporte_id=esporte_id_teste,
            dia_semana=dia_teste,
            hora_inicio=time(10, 0),
            hora_fim=time(22, 0),
            geom_localizacao=geom,
            raio_busca_km=15
        )
        db.add(nova_disp)
        
    db.commit()
    db.close()
    print("30 Jogadores criados com sucesso e prontos para o Matchmaking!")

if __name__ == "__main__":
    popular_banco_para_testes()