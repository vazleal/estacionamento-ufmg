import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

type Estatisticas = {
  total: number;
  reservadas_prof: number;
  ocupadas: number;
  professores: number;
  alunos: number;
  livres: number;
  livres_prof: number;
  alerta: boolean;
  bloquear_aluno: boolean;
};

function App() {
  const [stats, setStats] = useState<Estatisticas | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchStats = async () => {
    const res = await axios.get<Estatisticas>(
      "http://localhost:8000/estatisticas"
    );
    setStats(res.data);
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const registrar = async (
    tipo: "professor" | "aluno",
    acao: "entrada" | "saida"
  ) => {
    setLoading(true);
    try {
      await axios.post(`http://localhost:8000/${acao}/${tipo}`);
      await fetchStats();
    } catch (err: any) {
      alert(err.response?.data?.detail ?? "Erro ao registrar ação");
    } finally {
      setLoading(false);
    }
  };

  if (!stats) {
    return (
      <div className="app-container">
        <div className="loader"></div>
      </div>
    );
  }

  return (
    <div className="app-wrapper">
      <header className="header">
        <h1>
          Painel de Estacionamento <span>UFMG</span>
        </h1>
      </header>
      <main className="main-content">
        <div className="card">
          <section className="stats-grid">
            <div className="stat-item">
              <div className="stat-label">Total de Vagas</div>
              <div className="stat-value">{stats.total}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Disponíveis</div>
              <div className="stat-value">{stats.livres}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Ocupadas</div>
              <div className="stat-value">{stats.ocupadas}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Professores</div>
              <div className="stat-value">{stats.professores}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Alunos</div>
              <div className="stat-value">{stats.alunos}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Reservadas Professores</div>
              <div className="stat-value">{stats.reservadas_prof}</div>
            </div>
          </section>

          {stats.alerta && stats.professores < stats.reservadas_prof && (
            <div className="alert warning">
              ⚠️ Poucas vagas reservadas para professores!
            </div>
          )}

          {stats.bloquear_aluno && (
            <div className="alert error">🚫 Entrada de alunos bloqueada.</div>
          )}

          <section className="actions">
            <button
              className="btn btn-primary"
              disabled={loading}
              onClick={() => registrar("professor", "entrada")}
            >
              Entrada de Professor
            </button>
            <button
              className="btn btn-primary"
              disabled={loading || stats.bloquear_aluno}
              onClick={() => registrar("aluno", "entrada")}
            >
              Entrada de Aluno
            </button>
            <button
              className="btn btn-secondary"
              disabled={loading}
              onClick={() => registrar("professor", "saida")}
            >
              Saida de Professor
            </button>
            <button
              className="btn btn-secondary"
              disabled={loading}
              onClick={() => registrar("aluno", "saida")}
            >
              Saida de Aluno
            </button>
          </section>
        </div>
      </main>
      <footer className="footer">
        <p>Dados atualizados automaticamente a cada 5 segundos</p>
      </footer>
    </div>
  );
}

export default App;
