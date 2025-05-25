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

        professores       = dados.get("professor", 0)
        alunos            = dados.get("aluno", 0)
        total_ocupado     = professores + alunos
        vagas_restantes   = total_vagas - total_ocupado

        vagas_para_alunos = total_vagas - reservadas_prof
    
        vagas_restantes_alunos = vagas_para_alunos - alunos

        alerta = (
            professores < reservadas_prof
            and vagas_restantes_alunos <= reservadas_prof * aviso_limite
        )
        
        bloquear_aluno = vagas_restantes_alunos <= 0

        return Estatisticas(
            total=total_vagas,
            reservadas_prof=reservadas_prof,
            ocupadas=total_ocupado,
            professores=professores,
            alunos=alunos,
            livres=vagas_restantes,
            alerta=alerta,
            bloquear_aluno=bloquear_aluno
        )

router = APIRouter()

@router.get("/estatisticas", response_model=Estatisticas)
def painel():
    return get_estatisticas()