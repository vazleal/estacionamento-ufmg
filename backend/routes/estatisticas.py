from fastapi import APIRouter
from models import Estatisticas
from database import get_connection

def get_configuracoes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT total_vagas, reservadas_professores, aviso_limite FROM configuracoes WHERE id = 1")
        return cursor.fetchone()

def get_estatisticas():
    total_vagas, reservadas_prof, aviso_limite = get_configuracoes()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tipo, COUNT(*) FROM entradas GROUP BY tipo")
        dados = dict(cursor.fetchall())

        professores = dados.get("professor", 0)
        alunos = dados.get("aluno", 0)
        total_ocupado = professores + alunos

        vagas_restantes = total_vagas - total_ocupado
        vagas_restantes_prof = reservadas_prof - professores
        alerta = vagas_restantes_prof <= reservadas_prof * aviso_limite
        bloquear_aluno = total_ocupado >= total_vagas or vagas_restantes <= 0

        return Estatisticas(
            total=total_vagas,
            reservadas_prof=reservadas_prof,
            ocupadas=total_ocupado,
            professores=professores,
            alunos=alunos,
            livres=vagas_restantes,
            livres_prof=vagas_restantes_prof,
            alerta=alerta,
            bloquear_aluno=bloquear_aluno
        )

router = APIRouter()

@router.get("/estatisticas", response_model=Estatisticas)
def painel():
    return get_estatisticas()
