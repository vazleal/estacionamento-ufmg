# routes/configuracoes.py
from fastapi import APIRouter, Depends, HTTPException
from models import ConfiguracoesInput, ConfiguracoesOutput
from database import get_connection
from routes.usuarios import verificar_usuario_logado

router = APIRouter()

@router.get("/configuracoes", response_model=ConfiguracoesOutput)
def obter_configuracoes(user=Depends(verificar_usuario_logado)):
    if user["tipo"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito")
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
def atualizar_configuracoes(cfg: ConfiguracoesInput, user=Depends(verificar_usuario_logado)):
    if user["tipo"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE configuracoes
            SET total_vagas = ?, reservadas_professores = ?, aviso_limite = ?
            WHERE id = 1
        """, (cfg.total_vagas, cfg.reservadas_professores, cfg.aviso_limite))
        conn.commit()
    return {"status": "configurações atualizadas"}
