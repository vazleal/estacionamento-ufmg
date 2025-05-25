from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import get_connection
from routes.estatisticas import get_estatisticas

router = APIRouter()

@router.post("/entrada/{tipo}")
def registrar_entrada(tipo: str):
    if tipo not in ["professor", "aluno"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    stats = get_estatisticas()
    if tipo == "aluno" and stats.bloquear_aluno:
        raise HTTPException(status_code=403, detail="Entrada de aluno bloqueada: estacionamento cheio")
    agora = datetime.now()
    dia_semana = agora.strftime('%A')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO entradas (tipo, data_hora, dia_semana) VALUES (?, ?, ?)",
            (tipo, agora.isoformat(), dia_semana)
        )
        conn.commit()
    return {"status": "entrada registrada"}

@router.post("/saida/{tipo}")
def registrar_saida(tipo: str):
    if tipo not in ["professor", "aluno"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM entradas WHERE tipo = ? ORDER BY id DESC LIMIT 1",
            (tipo,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Nenhuma entrada de {tipo} encontrada para saída"
            )
        last_id = row[0]
        cursor.execute("DELETE FROM entradas WHERE id = ?", (last_id,))
        conn.commit()
    return {"status": "saida registrada"}
