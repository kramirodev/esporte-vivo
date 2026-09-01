from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime, time
from decimal import Decimal

# ==========================================
# MÓDULO 1: IDENTIDADE
# ==========================================

class UsuarioCreate(BaseModel):
    telefone: str = Field(..., max_length=20)
    nome: str = Field(..., max_length=100)
    apelido: str = Field(..., max_length=50)
    latitude: Optional[float] 
    longitude: Optional[float]

class UsuarioResponse(BaseModel):
    id: UUID
    api_key: UUID
    telefone: str
    nome: str
    trust_factor: int
    status_conta: str
    is_premium: bool
    premium_vence_em: Optional[datetime]
    criado_em: datetime
    geom_localizacao: Optional[str] = None
    apelido: str

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 2: ESPORTES E GAMIFICAÇÃO
# ==========================================

class EsporteCreate(BaseModel):
    nome: str = Field(..., max_length=50)
    jogadores_por_time: int

class EsporteResponse(BaseModel):
    id: int
    nome: str
    jogadores_por_time: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)

class VincularEsportesRequest(BaseModel):
    esporte_ids: list[int]

class UsuarioEloCreate(BaseModel):
    esporte_id: int

class UsuarioEloResponse(BaseModel):
    usuario_id: UUID
    esporte_id: int
    pontuacao_elo: int
    partidas_jogadas: int
    vitorias: int
    derrotas: int

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 3: DISPONIBILIDADE
# ==========================================

class JanelaTempo(BaseModel):
    dia_semana: int = Field(..., ge=0, le=6)
    hora_inicio: time
    hora_fim: time

class DisponibilidadePadraoCreate(BaseModel):
    esporte_id: int
    horarios: list[JanelaTempo] 
    latitude: float
    longitude: float
    raio_busca_km: Optional[int] = 10

class DisponibilidadePadraoResponse(BaseModel):
    id: UUID
    esporte_id: int
    dia_semana: int
    hora_inicio: time
    hora_fim: time
    geom_localizacao: Optional[str] = None
    raio_busca_km: int

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 4: INFRAESTRUTURA
# ==========================================

class LocalPartidaCreate(BaseModel):
    nome: str = Field(..., max_length=100)
    tipo_local: str = Field(..., max_length=20)
    latitude: float
    longitude: float
    endereco: Optional[str] = Field(None, max_length=255)
    valor_hora: Optional[Decimal] = Decimal('0.00')

class LocalPartidaResponse(BaseModel):
    id: UUID
    nome: str
    tipo_local: str
    geom_localizacao: str
    endereco: Optional[str]
    valor_hora: Decimal
    ativo: bool

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 5: PARTIDAS
# ==========================================

class PartidaCreate(BaseModel):
    esporte_id: int
    local_id: UUID
    tipo: Optional[str] = 'casual'
    data_hora_agendada: datetime

class PartidaResponse(BaseModel):
    id: UUID
    esporte_id: int
    local_id: UUID
    tipo: str
    status: str
    data_hora_agendada: datetime
    elo_medio: Optional[int]
    time_vencedor: str

    model_config = ConfigDict(from_attributes=True)


class PartidaJogadorCreate(BaseModel):
    partida_id: UUID
    usuario_id: UUID
    time_alocado: str = Field(..., max_length=5)

class PartidaJogadorResponse(BaseModel):
    partida_id: UUID
    usuario_id: UUID
    time_alocado: str
    compareceu: bool
    variacao_elo_obtida: int

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 6: CONSENSO E ANTI-FRAUDE
# ==========================================

class VotoPartidaCreate(BaseModel):
    partida_id: UUID
    voto_resultado: str = Field(..., max_length=20)

class VotoPartidaResponse(BaseModel):
    partida_id: UUID
    usuario_id: UUID
    voto_resultado: str
    data_voto: datetime

    model_config = ConfigDict(from_attributes=True)


class DenunciaReportCreate(BaseModel):
    denunciado_id: UUID
    partida_id: UUID
    motivo: str = Field(..., max_length=50)

class DenunciaReportResponse(BaseModel):
    id: UUID
    denunciante_id: UUID
    denunciado_id: UUID
    partida_id: UUID
    motivo: str
    status_analise: str

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 7: COSMÉTICOS
# ==========================================

class ItemCosmeticoCreate(BaseModel):
    tipo_item: str = Field(..., max_length=30)
    nome: str = Field(..., max_length=50)
    caminho_asset: str = Field(..., max_length=255)

class ItemCosmeticoResponse(BaseModel):
    id: int
    tipo_item: str
    nome: str
    caminho_asset: str

    model_config = ConfigDict(from_attributes=True)


class InventarioUsuarioCreate(BaseModel):
    item_id: int

class InventarioUsuarioResponse(BaseModel):
    usuario_id: UUID
    item_id: int
    equipado: bool

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# MÓDULO 8: REDIS + FILA
# ==========================================

class EntrarFilaRequest(BaseModel):
    esporte_ids: list[int]

class FilaResponse(BaseModel):
    sucesso: bool
    mensagem: str
    detalhes: dict | None = None