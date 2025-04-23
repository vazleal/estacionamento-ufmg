# routes/configuracoes.py
from fastapi import APIRouter
from models import ConfiguracoesInput, ConfiguracoesOutput
from database import get_connection

router = APIRouter()

@router.get("/configuracoes", response_model=ConfiguracoesOutput)
def obter_configuracoes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT total_vagas, reservadas_professores, aviso_limite FROM configuracoes WHERE id = 1")
        row = cursor.fetchone()
    return ConfiguracoesOutput(
        total_vagas=row[0],
        reservadas_professores=row[1],
        aviso_limite=row[2]
    )

@router.put("/configuracoes")
def atualizar_configuracoes(cfg: ConfiguracoesInput):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE configuracoes
            SET total_vagas = ?, reservadas_professores = ?, aviso_limite = ?
            WHERE id = 1
        """, (cfg.total_vagas, cfg.reservadas_professores, cfg.aviso_limite))
        conn.commit()
    return {"status": "configurações atualizadas"}
