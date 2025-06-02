from typing import List
from fastapi import APIRouter, HTTPException
from models import UsuarioInput, UsuarioOutput, LoginInput, VeiculoInput, VeiculoOutput
from database import get_connection

router = APIRouter()

@router.post("/register", response_model=UsuarioOutput)
def register(user: UsuarioInput):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, email, senha, matricula)
                VALUES (?, ?, ?, ?)
            """, (user.nome, user.email, user.senha, user.matricula))
            conn.commit()
            user_id = cursor.lastrowid
        except Exception:
            raise HTTPException(status_code=400, detail="Usuário já existe")
    return UsuarioOutput(id=user_id, nome=user.nome, email=user.email, matricula=user.matricula)

@router.post("/login", response_model=UsuarioOutput)
def login(cred: LoginInput):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, email, matricula FROM usuarios
            WHERE email = ? AND senha = ?
        """, (cred.email, cred.senha))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return UsuarioOutput(id=user[0], nome=user[1], email=user[2], matricula=user[3])

@router.post("/usuario/{usuario_id}/veiculos", response_model=VeiculoOutput)
def add_veiculo(usuario_id: int, veiculo: VeiculoInput):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO veiculos (usuario_id, placa)
            VALUES (?, ?)
        """, (usuario_id, veiculo.placa))
        conn.commit()
        veiculo_id = cursor.lastrowid
    return VeiculoOutput(id=veiculo_id, placa=veiculo.placa)

@router.get("/usuario/{usuario_id}/veiculos", response_model=List[VeiculoOutput])
def listar_veiculos(usuario_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, placa FROM veiculos WHERE usuario_id = ?
        """, (usuario_id,))
        rows = cursor.fetchall()
    return [VeiculoOutput(id=row[0], placa=row[1]) for row in rows]
