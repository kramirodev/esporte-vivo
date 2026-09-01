from uuid import UUID

from app.services import matchmaking_worker


class _FakeQuery:
    def __init__(self, usuario_ativos=None):
        self.usuario_ativos = usuario_ativos or set()

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return [(usuario_id,) for usuario_id in sorted(self.usuario_ativos, key=str)]


class _FakeDB:
    def __init__(self, usuario_ativos=None):
        self.usuario_ativos = usuario_ativos or set()

    def query(self, *args, **kwargs):
        return _FakeQuery(self.usuario_ativos)


def test_filtrar_jogadores_ja_em_partida_ativa_remove_jogadores_ativos():
    jogadores = [
        ("11111111-1111-1111-1111-111111111111", 1800, "A"),
        ("22222222-2222-2222-2222-222222222222", 1700, "A"),
        ("33333333-3333-3333-3333-333333333333", 1600, "B"),
    ]
    db = _FakeDB({UUID("11111111-1111-1111-1111-111111111111")})

    resultado = matchmaking_worker._filtrar_jogadores_ja_em_partida_ativa(db, jogadores)

    assert [j[0] for j in resultado] == [
        "22222222-2222-2222-2222-222222222222",
        "33333333-3333-3333-3333-333333333333",
    ]


def test_filtrar_jogadores_ja_em_partida_ativa_remove_duplicados():
    jogadores = [
        ("11111111-1111-1111-1111-111111111111", 1800, "A"),
        ("11111111-1111-1111-1111-111111111111", 1800, "A"),
        ("22222222-2222-2222-2222-222222222222", 1700, "B"),
    ]
    db = _FakeDB(set())

    resultado = matchmaking_worker._filtrar_jogadores_ja_em_partida_ativa(db, jogadores)

    assert [j[0] for j in resultado] == [
        "11111111-1111-1111-1111-111111111111",
        "22222222-2222-2222-2222-222222222222",
    ]
