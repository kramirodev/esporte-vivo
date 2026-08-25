import random
from datetime import time
from sqlalchemy import func
from app.database.conexao import _sessionLocal
from app.database import models

def popular_banco_para_testes():
    db = _sessionLocal()
    
    esporte_id_teste = 1  
    dia_teste = 6         
    
    for i in range(1, 31):
        # Gera coordenadas próximas umas das outras raio de aprox. 5km a 10km
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
        
        # Cria o Elo pontuação aleatória entre 800 e 2200
        elo_aleatorio = random.randint(800, 2200)
        
        partidas_jogadas = random.randint(6,25)

        partidas_vencidas = random.randint(1,partidas_jogadas)

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
        
        # Cria a Disponibilidade  - Livre das 10h às 22h
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
    print("✅ 30 Jogadores criados com sucesso e prontos para o Matchmaking!")

if __name__ == "__main__":
    popular_banco_para_testes()