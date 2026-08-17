import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv('DB_NAME') ,
    "user": os.getenv('DB_USER'), 
    "password": os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
} \

SCHEMA_SQL = """
-- Ativa a extensão espacial para as coordenadas
CREATE EXTENSION IF NOT EXISTS postgis;

-- MÓDULO 1: IDENTIDADE

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_key UUID UNIQUE DEFAULT gen_random_uuid(),
    telefone VARCHAR(20) UNIQUE NOT NULL,
    apelido VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    trust_factor INT DEFAULT 100,
    status_conta VARCHAR(20) DEFAULT 'ativo',
    is_premium BOOLEAN DEFAULT FALSE,
    premium_vence_em TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    geom_localizacao GEOMETRY(Point, 4326)
);

-- MÓDULO 2: ESPORTES E GAMIFICAÇÃO
CREATE TABLE esportes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    jogadores_por_time INT NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE usuario_elo (
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    esporte_id INT REFERENCES esportes(id) ON DELETE CASCADE,
    pontuacao_elo INT DEFAULT 1000,
    partidas_jogadas INT DEFAULT 0,
    vitorias INT DEFAULT 0,
    derrotas INT DEFAULT 0,
    PRIMARY KEY (usuario_id, esporte_id)
);

-- MÓDULO 3: DISPONIBILIDADE
CREATE TABLE disponibilidade_padrao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    esporte_id INT REFERENCES esportes(id) ON DELETE CASCADE,
    dia_semana INT CHECK (dia_semana >= 0 AND dia_semana <= 6),
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    geom_localizacao GEOMETRY(Point, 4326),
    raio_busca_km INT DEFAULT 10
);

-- MÓDULO 4: INFRAESTRUTURA
CREATE TABLE locais_partida (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL,
    tipo_local VARCHAR(20) NOT NULL,
    geom_localizacao GEOMETRY(Point, 4326) NOT NULL,
    endereco VARCHAR(255),
    valor_hora DECIMAL(10, 2) DEFAULT 0.00,
    ativo BOOLEAN DEFAULT TRUE
);

-- MÓDULO 5: PARTIDAS
CREATE TABLE partidas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    esporte_id INT REFERENCES esportes(id),
    local_id UUID REFERENCES locais_partida(id),
    tipo VARCHAR(20) DEFAULT 'casual',
    status VARCHAR(30) DEFAULT 'formada',
    data_hora_agendada TIMESTAMP NOT NULL,
    elo_medio INT,
    time_vencedor VARCHAR(10) DEFAULT 'aguardando'
);

CREATE TABLE partida_jogadores (
    partida_id UUID REFERENCES partidas(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    time_alocado VARCHAR(5) NOT NULL,
    compareceu BOOLEAN DEFAULT TRUE,
    variacao_elo_obtida INT DEFAULT 0,
    PRIMARY KEY (partida_id, usuario_id)
);

-- MÓDULO 6: CONSENSO E ANTI-FRAUDE
CREATE TABLE votos_partida (
    partida_id UUID REFERENCES partidas(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    voto_resultado VARCHAR(20) NOT NULL,
    data_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (partida_id, usuario_id)
);

CREATE TABLE denuncias_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    denunciante_id UUID REFERENCES usuarios(id),
    denunciado_id UUID REFERENCES usuarios(id),
    partida_id UUID REFERENCES partidas(id),
    motivo VARCHAR(50) NOT NULL,
    status_analise VARCHAR(20) DEFAULT 'pendente'
);

-- MÓDULO 7: COSMÉTICOS
CREATE TABLE itens_cosmeticos (
    id SERIAL PRIMARY KEY,
    tipo_item VARCHAR(30) NOT NULL,
    nome VARCHAR(50) NOT NULL,
    caminho_asset VARCHAR(255) NOT NULL
);

CREATE TABLE inventario_usuario (
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    item_id INT REFERENCES itens_cosmeticos(id) ON DELETE CASCADE,
    equipado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (usuario_id, item_id)
);
"""

def inicializar_banco():
    try:
        conexao = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )

        conexao.set_client_encoding('UTF8')
        
        cursor = conexao.cursor()
        
        print("Criando tabelas e extensões no banco de dados...")
        
        cursor.execute(SCHEMA_SQL)
        
        conexao.commit()
        print("Arquitetura criada com sucesso!")
        
        
    except Exception as e:
        print(f"Erro ao conectar ou criar tabelas: {repr(e)}")
        
    finally:
        if 'conexao' in locals():
            cursor.close() # type: ignore
            conexao.close() # type: ignore

if __name__ == "__main__":
    inicializar_banco()