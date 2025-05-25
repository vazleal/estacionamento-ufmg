# models.py
from pydantic import BaseModel

class Estatisticas(BaseModel):
    total: int
    reservadas_prof: int
    ocupadas: int
    professores: int
    alunos: int
    livres: int
    alerta: bool
    bloquear_aluno: bool

class ConfiguracoesInput(BaseModel):
    total_vagas: int
    reservadas_professores: int
    aviso_limite: float

class ConfiguracoesOutput(BaseModel):
    total_vagas: int
    reservadas_professores: int
    aviso_limite: float
