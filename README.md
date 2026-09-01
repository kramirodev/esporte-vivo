# Esporte Vivo

Projeto de backend para um sistema de matchmaking esportivo amador, com foco em partidas automáticas, balanceamento por MMR e uso de geolocalização.

Este repositório representa a versão funcional atual da API e do motor de matchmaking em desenvolvimento.

## Visão geral

A ideia central do projeto é formar partidas automaticamente com base em:

- esporte
- localização
- disponibilidade de horário
- nível técnico / MMR
- equilíbrio entre os times
- eventos em tempo real para jogadores conectados

## Stack atual

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL + PostGIS
- Redis
- WebSockets
- asyncio

### Estrutura atual do sistema
- API REST para usuários, esportes, disponibilidade e fila
- worker em Python para processar filas e formar partidas
- armazenamento temporário da fila em Redis
- persistência de partidas no PostgreSQL
- WebSocket para notificar jogadores sobre partidas formadas

## Arquitetura atual

```text
Cliente / App futuro
        |
        | REST + WebSocket
        v
FastAPI API
  - usuários
  - esportes
  - locais
  - disponibilidade
  - fila
  - partidas
        |
        +-------------------+
        |                   |
        v                   v
PostgreSQL + PostGIS    Redis
  - usuários             - fila por esporte
  - partidas            - MMR por jogador
  - disponibilidade     - filas ativas
  - locais              - lock de processamento

        |
        v
Worker de Matchmaking
  - lê filas no Redis
  - seleciona jogadores
  - valida balanceamento
  - cria partida no banco
  - remove jogadores da fila
  - notifica por WebSocket
```

## O que já existe hoje

### API
- cadastro e consulta de usuários
- cadastro de esportes
- cadastro de locais
- cadastro de disponibilidade por usuário
- entrada e saída da fila
- consulta do status da fila
- criação inicial de partidas
- alocação de jogadores na partida

### Banco de dados
- esquema inicial em PostgreSQL
- suporte a geolocalização com PostGIS
- tabelas para usuários, esportes, disponibilidade, locais e partidas

### Redis
- filas por esporte em ZSET
- conjunto de usuários em fila
- hash de MMR por esporte
- conjunto de filas ativas
- lock de processamento por esporte

### Matchmaking
- leitura da fila
- ordenação por MMR
- seleção de jogadores para times
- validação da qualidade da partida
- formação inicial de times A/B
- remoção dos jogadores da fila após partida formada

### WebSocket
- gerenciamento de conexões por usuário
- envio de eventos para jogadores

## O que ainda não é prioridade real

O projeto ainda não está em nível de produto final. O que ainda não existe ou está incompleto:

- autenticação real de usuários (hoje usa API key simples)
- frontend ou app mobile
- Kafka implementado
- ranking e atualização de MMR após partida
- painel administrativo completo
- testes de integração completos
- deploy real em produção

## Estrutura do projeto

```text
app/
  database/
    models.py
    redis_conexao.py
    schemas.py
    sqlalchemy_conexao.py
    setup_batabase_SQL.py
  routers/
    disponibilidade.py
    esportes.py
    fila.py
    locais.py
    partidas.py
    user.py
    websocket.py
  services/
    matchmaking.py
    matchmaking_worker.py
    mmr.py
    websocket_manager.py

main.py
worker.py
compose.yaml
dockerfile
requirements.txt
.env.example
```

## Como rodar localmente

### 1. instale as dependências

```bash
pip install -r requirements.txt
```

### 2. configure o ambiente

Copie o exemplo:

```bash
copy .env.example .env
```

Preencha os valores do banco e do Redis antes de subir os serviços.

### 3. suba o banco e o Redis

```bash
docker compose up -d db redis
```

### 4. rode a API

```bash
uvicorn main:app --reload
```

### 5. rode o worker

```bash
python worker.py
```

## Observações importantes

- o worker foi separado do processo da API para deixar o runtime mais organizado
- o projeto ainda está em fase de backend e matchmaking core
- o README foi atualizado para refletir o estado real do código, e não o roadmap idealizado

## Licença

Todos os direitos reservados.

Este projeto foi criado como base para estudo, portfólio e evolução técnica.
