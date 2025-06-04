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

@router.put("/usuario/{usuario_id}/veiculos/{veiculo_id}", response_model=VeiculoOutput)
def update_veiculo(usuario_id: int, veiculo_id: int, veiculo_data: VeiculoInput):
    with get_connection() as conn:
        cursor = conn.cursor()
        # Verificar se o veículo existe e pertence ao usuário
        cursor.execute("SELECT id FROM veiculos WHERE id = ? AND usuario_id = ?", (veiculo_id, usuario_id))
        existing_veiculo = cursor.fetchone()
        if not existing_veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado ou não pertence ao usuário")

        try:
            cursor.execute("""
                UPDATE veiculos
                SET placa = ?
                WHERE id = ? AND usuario_id = ?
            """, (veiculo_data.placa.upper(), veiculo_id, usuario_id))
            conn.commit()
        except Exception as e: # Tratar possível duplicidade de placa ao atualizar
            conn.rollback()
            print(f"Erro ao atualizar veículo: {e}")
            raise HTTPException(status_code=409, detail=f"Já existe um veículo com a placa '{veiculo_data.placa.upper()}' para este usuário ou outro erro.")

        if cursor.rowcount == 0: # Nenhum registro foi atualizado
             raise HTTPException(status_code=404, detail="Veículo não encontrado para atualização")
    return VeiculoOutput(id=veiculo_id, placa=veiculo_data.placa.upper())

@router.delete("/usuario/{usuario_id}/veiculos/{veiculo_id}", status_code=204)
def delete_veiculo(usuario_id: int, veiculo_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        # Verificar se o veículo existe e pertence ao usuário
        cursor.execute("SELECT id FROM veiculos WHERE id = ? AND usuario_id = ?", (veiculo_id, usuario_id))
        existing_veiculo = cursor.fetchone()
        if not existing_veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado ou não pertence ao usuário")

        cursor.execute("""
            DELETE FROM veiculos
            WHERE id = ? AND usuario_id = ?
        """, (veiculo_id, usuario_id))
        conn.commit()
        if cursor.rowcount == 0: # Nenhum registro foi deletado
            raise HTTPException(status_code=404, detail="Veículo não encontrado para exclusão")
    return # Retorna 204 No Content