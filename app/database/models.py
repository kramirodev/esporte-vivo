from sqlalchemy.ext.automap import automap_base
from models import engine

_base = automap_base()
_base.prepare(autoload_with=engine)

# Mapeamento das tabelas
denuncia_report = _base.classes.denuncias_reports
disponibilidade_padrao = _base.classes.disponibilidade_padrao
esporte = _base.classes.esportes
inventario_usuario = _base.classes.inventario_usuario
item_cosmetico = _base.classes.itens_cosmeticos
local_partida = _base.classes.locais_partida
partida_jogador = _base.classes.partida_jogadores
partida = _base.classes.partidas
spatial_ref_sys = _base.classes.spatial_ref_sys  # Tabela interna do PostGIS
usuario_elo = _base.classes.usuario_elo
user = _base.classes.usuarios
voto_partida = _base.classes.votos_partida

