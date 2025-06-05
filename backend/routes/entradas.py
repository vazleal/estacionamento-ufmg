from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from database import get_connection
from routes.estatisticas import get_estatisticas
from models import PlacaInput
from routes.usuarios import verificar_usuario_logado

router = APIRouter()

@router.post("/entrada")
def registrar_entrada(placa_info: PlacaInput, user=Depends(verificar_usuario_logado)):
    if user["tipo"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito")

    placa = placa_info.placa
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT u.tipo FROM veiculos v JOIN usuarios u ON v.usuario_id = u.id WHERE v.placa = ?",
            (placa,),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Veículo não cadastrado")
        tipo = row[0]
        cursor.execute("SELECT id FROM entradas WHERE placa = ?", (placa,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Veículo já está no estacionamento")

    stats = get_estatisticas()
    if stats.livres <= 0:
        raise HTTPException(status_code=403, detail="Estacionamento cheio: não há vagas disponíveis")
    if tipo == "aluno" and stats.bloquear_aluno:
        raise HTTPException(status_code=403, detail="Entrada de aluno bloqueada: limite de vagas para alunos atingido")

    agora = datetime.now()
    dia_semana = agora.strftime('%A')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO entradas (tipo, placa, data_hora, dia_semana) VALUES (?, ?, ?, ?)",
            (tipo, placa, agora.isoformat(), dia_semana),
        )
        conn.commit()
    return {"status": "entrada registrada"}

@router.post("/saida")
def registrar_saida(placa_info: PlacaInput, user=Depends(verificar_usuario_logado)):
    if user["tipo"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito")

    placa = placa_info.placa
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, tipo FROM entradas WHERE placa = ? ORDER BY id DESC LIMIT 1",
            (placa,),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Nenhuma entrada encontrada para essa placa")
        entrada_id, tipo = row
        cursor.execute("DELETE FROM entradas WHERE id = ?", (entrada_id,))
        conn.commit()
    return {"status": "saida registrada", "tipo": tipo}
