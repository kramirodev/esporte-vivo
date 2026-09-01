from dataclasses import dataclass
from statistics import mean


def peso_elo(pontuacao: int) -> float:
    if pontuacao >= 4000:
        return 1.00
    if pontuacao >= 3500:
        return 0.95
    if pontuacao >= 3000:
        return 0.90
    if pontuacao >= 2500:
        return 0.85
    if pontuacao >= 2000:
        return 0.80
    if pontuacao >= 1500:
        return 0.70
    if pontuacao >= 1000:
        return 0.65
    if pontuacao >= 500:
        return 0.60
    return 0.55


@dataclass(frozen=True)
class ResultadoMatch:
    probabilidade_time_a: float
    brier_score: float
    quality_score: float
    aprovado: bool


def avaliar_times(pesos_time_a: list[float], pesos_time_b: list[float], limite_brier: float = 0.08) -> ResultadoMatch:
    return avaliar_partida(pesos_time_a, pesos_time_b, limite_brier)


def avaliar_partida(
    pesos_time_a: list[float],
    pesos_time_b: list[float],
    limite_brier: float = 0.08
) -> ResultadoMatch:
    if not pesos_time_a or not pesos_time_b:
        raise ValueError('Os dois times precisam possuir jogadores.')

    media_a = mean(pesos_time_a)
    media_b = mean(pesos_time_b)

    # Converte a diferença relativa dos pesos em probabilidade esperada.
    probabilidade_a = media_a / (media_a + media_b)

    # Brier Score contra o resultado neutro esperado (0.5).
    brier = (probabilidade_a - 0.5) ** 2
    quality = max(0.0, 1.0 - (brier / limite_brier))

    return ResultadoMatch(
        probabilidade_time_a=probabilidade_a,
        brier_score=brier,
        quality_score=quality,
        aprovado=brier <= limite_brier
    )
