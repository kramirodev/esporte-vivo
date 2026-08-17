import random as r

peso = {
    1: 1.00,  # Challenger
    2: 0.95,  # Grandmaster
    3: 0.90,  # Master
    4: 0.85,  # Diamond
    5: 0.80,  # Platinum
    6: 0.70,  # Gold
    7: 0.65,  # Silver
    8: 0.60,  # Bronze
    9: 0.55   # Iron
}

fila_jogadores = [
    {"nome": "FalleN", "mmr": 4200, "elo_id": 1, "peso": None, "mmr_ponderado": None},
    {"nome": "Coldzera", "mmr": 4050, "elo_id": 1, "peso": None, "mmr_ponderado": None},
    {"nome": "Fer", "mmr": 3800, "elo_id": 2, "peso": None, "mmr_ponderado": None},
    {"nome": "TACO", "mmr": 3600, "elo_id": 2, "peso": None, "mmr_ponderado": None},
    {"nome": "fnx", "mmr": 3200, "elo_id": 3, "peso": None, "mmr_ponderado": None},
    {"nome": "KSCERATO", "mmr": 3100, "elo_id": 3, "peso": None, "mmr_ponderado": None},
    {"nome": "Yuurih", "mmr": 2400, "elo_id": 4, "peso": None, "mmr_ponderado": None},
    {"nome": "Art", "mmr": 2350, "elo_id": 4, "peso": None, "mmr_ponderado": None},
    {"nome": "Drop", "mmr": 2100, "elo_id": 4, "peso": None, "mmr_ponderado": None},
    {"nome": "Saffee", "mmr": 1900, "elo_id": 5, "peso": None, "mmr_ponderado": None},
    {"nome": "Chelo", "mmr": 1850, "elo_id": 5, "peso": None, "mmr_ponderado": None},
    {"nome": "Boltz", "mmr": 1600, "elo_id": 6, "peso": None, "mmr_ponderado": None},
    {"nome": "VINI", "mmr": 1550, "elo_id": 6, "peso": None, "mmr_ponderado": None},
    {"nome": "Nqz", "mmr": 1400, "elo_id": 6, "peso": None, "mmr_ponderado": None},
    {"nome": "Dumau", "mmr": 1250, "elo_id": 7, "peso": None, "mmr_ponderado": None},
    {"nome": "B4rtiN", "mmr": 1150, "elo_id": 7, "peso": None, "mmr_ponderado": None},
    {"nome": "Latto", "mmr": 900,  "elo_id": 8, "peso": None, "mmr_ponderado": None},
    {"nome": "Wood7", "mmr": 850,  "elo_id": 8, "peso": None, "mmr_ponderado": None},
    {"nome": "Tuurtle", "mmr": 600,  "elo_id": 9, "peso": None, "mmr_ponderado": None},
    {"nome": "Pesadelo", "mmr": 450,  "elo_id": 9, "peso": None, "mmr_ponderado": None}
]

def peso_mmr_unico(jogador):
    elo_peso = jogador['mmr'] * peso[jogador['elo_id']]
    
    jogador['mmr_ponderado'] = int(elo_peso)
    jogador['peso'] = peso[jogador['elo_id']]

###organizar com sorted
###verificar se o limiar minimo de ponto existe no mmr
###verificar por impares e pares para formar times

def formar_partida(fila):
    fila_ordenada = sorted(fila, key=lambda jogador: jogador['mmr_ponderado'], reverse = True)

    lobby = fila_ordenada[:10]

    mmr_max = lobby[0]['mmr_ponderado']
    mmr_min = lobby[9]['mmr_ponderado']

    if mmr_max - mmr_min > 2700:
        print(f'Diferença de MMR ponderado: {mmr_max - mmr_min}')
        print("Diferença de nível muito alta! Aguardando mais jogadores...")
        return None

    print ("Lobby formado")

    time_azul = []
    time_vermelho = []

    indice_azul = [0,3,4,7,8]

    for i, jogador, in enumerate(lobby):
        if i in indice_azul:
            time_azul.append(jogador)
        else:
            time_vermelho.append(jogador)

    media_azul = sum(jogador['mmr_ponderado'] for jogador in time_azul)/5
    media_vermelha = sum(jogador['mmr_ponderado'] for jogador in time_vermelho)/5

    print('==== Time azul ====')

    for jogador in time_azul:
        print(f"{jogador['nome']} - MMR PONDERADO: {jogador['mmr_ponderado']}) - MMR: {jogador['mmr']}") 

    print(f'Média do time: {media_azul:.0f}\n')

    print('==== Time vermelho ====')

    for jogador in time_vermelho:
        print(f"{jogador['nome']} - MMR PONDERADO: {jogador['mmr_ponderado']}) - MMR: {jogador['mmr']}") 

    print(f'Média do time: {media_vermelha:.0f}\n')

for i, jogador in enumerate(fila_jogadores):
    peso_mmr_unico(jogador)
###    print(jogador)

formar_partida(fila_jogadores)