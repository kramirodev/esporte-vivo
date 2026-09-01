# Esporte Vivo

O Esporte Vivo é uma plataforma inovadora de matchmaking ativo e assíncrono para esportes coletivos amadores. Inspirada na lógica de eSports, a aplicação elimina a barreira logística de organizar partidas, operando em segundo plano para formar "lobbies" automatizados com base em disponibilidade de horário, geolocalização e nível técnico (Elo).

---

## Principais Recursos e Funcionalidades

- **Fila de Matchmaking Ativo:** O usuário informa sua disponibilidade (dias, faixas de horário e raio geográfico) e o sistema cruza esses dados em segundo plano.
- **Sistema de Elo (Gamificação):** Separação entre partidas Casuais e Ranqueadas. O cálculo de MMR/Elo equilibra os times para criar confrontos justos e alimenta um Leaderboard regional.
- **Validação de Resultados e Anti-Fraude:**
  - **Voto de Maioria:** Confirmação descentralizada do resultado da partida por consenso entre os jogadores.
  - **Trust Factor (Score de Confiança):** Vinculado ao número de celular, punindo W.O.s e tentativas de fraude com degradação do score ou exclusão de filas ranqueadas.
- **Alocação de Locais:** Mapeamento de quadras públicas (gratuitas) e integração com complexos esportivos pagos (com reserva e divisão de custos).
- **Modelo de Negócios e Monetização:**
  - **B2B:** Integração com quadras privadas para preenchimento de horários ociosos.
  - **Assinatura Premium:** Benefícios cosméticos (bordas, badges, títulos) e prioridade em filas sem interferir no balanceamento do Elo.
  - **Eventos:** Torneios físicos oficiais ("Copa de Fim de Temporada") ao congelar o ranking.

---

## Arquitetura e Tecnologias Projetadas

O ecossistema é baseado em uma arquitetura preparada para evolução em serviços independentes e processamento assíncrono:

- **Backend:** Python (FastAPI/Flask) para consumo de REST API e WebSockets em tempo real.
- **Banco de Dados Relacional:** PostgreSQL com extensão PostGIS para filtros geográficos.
- **Fila em Tempo Real:** Redis para gerenciamento da sala de espera dos jogadores.
- **Worker de Matchmaking:** Script em segundo plano dedicado ao consumo da fila do Redis e execução dos algoritmos de equilíbrio de MMR para formação das partidas.
- **Mensageria & Eventos:** Apache Kafka para notificação assíncrona entre o motor de matchmaking e os serviços da API (próxima etapa).
- **Containerização:** Docker e Docker Compose para orquestração de ambiente.

---

## Status do Desenvolvimento (Fase Atual)

O projeto concluiu as bases do backend e do motor de processamento assíncrono, operando atualmente até a camada do Worker consumindo do Redis. 

### O que já está implementado:
1. **Regra de Negócio e Algoritmo Core:** Lógica matemática de divisão de times por proximidade de MMR e limite de discrepância.
2. **API Backend:** Rotas construídas para inserção e remoção de jogadores, separando a lógica da API das funções do motor de matchmaking.
3. **Banco de Dados:** Tabelas e relacionamentos modelados (PostgreSQL), substituindo o armazenamento de variáveis em memória.
4. **Fila e Worker (Redis):** Integração das rotas da API com o Redis, atuando como sala de espera. O Worker em segundo plano já consome esta fila, aplica a regra de MMR para formar a partida quando o quórum é alcançado, salva os dados no banco e limpa os usuários alocados.

---

## Roadmap de Desenvolvimento

- [x] Fase 1: Algoritmo base de balanceamento por MMR e versionamento.
- [x] Fase 2: Criação da API (Backend Base) com endpoints de fila.
- [x] Fase 3: Banco de Dados PostgreSQL/PostGIS (Tabelas de Jogadores, Locais e Disponibilidade).
- [x] Fase 4: Integração com Redis para gerenciamento de fila em tempo real.
- [x] Fase 5: Implementação do Worker de Matchmaking consumindo dados do Redis em loop.
- [ ] Fase 6: Comunicação entre serviços com Apache Kafka (Producer no Worker e Consumer na API).
- [ ] Fase 7: Orquestração e Ambiente Completo com Docker Compose unificando todos os serviços.
- [ ] Fase 8: Interface do Usuário com WebSockets para atualização em tempo real.
- [ ] Fase 9: Testes automatizados de carga e ajustes finos de balanceamento.
- [ ] Fase 10: Deploy na nuvem da API, Banco, Redis, Kafka e Frontend.

---

## Licença

**Todos os Direitos Reservados (All Rights Reserved)**

O código-fonte deste projeto é disponibilizado em repositório público única e exclusivamente para fins de leitura e portfólio. 
É estritamente proibido o uso, cópia, modificação, distribuição, compilação ou exploração comercial de qualquer parte deste projeto sem a autorização prévia, expressa e por escrito do autor.
