# models.py
from pydantic import BaseModel, validator
import re

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

class UsuarioInput(BaseModel):
    nome: str
    email: str
    senha: str
    matricula: str
    tipo: str

class UsuarioOutput(BaseModel):
    id: int
    nome: str
    email: str
    matricula: str
    tipo: str

class LoginInput(BaseModel):
    email: str
    senha: str

class VeiculoInput(BaseModel):
    placa: str

class VeiculoOutput(BaseModel):
    id: int
    placa: str

class PlacaInput(BaseModel):
    placa: str

    @validator('placa')
    def validar_placa(cls, v: str) -> str:
        v = v.upper()
        if not re.fullmatch(r'[A-Z0-9]{7}', v):
            raise ValueError('Placa inválida')
        return v

class UpdateTipoInput(BaseModel):
    email: str
    tipo: str
