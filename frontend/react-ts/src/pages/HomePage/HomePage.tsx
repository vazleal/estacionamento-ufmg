import axios from "axios";
import { useEffect, useState } from "react";

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

export const HomePage = () => {
    const [stats, setStats] = useState<Estatisticas | null>(null);
    const [loading, setLoading] = useState(false);
    const [placa, setPlaca] = useState("");

    useEffect(() => {
        const tipo = localStorage.getItem("usuario_tipo");
        if (tipo !== "admin") {
            window.location.href = "/painel";
        }
    }, []);

    const fetchStats = async () => {
        const res = await axios.get<Estatisticas>(
            "http://localhost:8000/estatisticas",
            { headers: { "X-Usuario-Id": localStorage.getItem("usuario_id") || "" } }
        );
        setStats(res.data);
    };

    useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 5000);
        return () => clearInterval(interval);
    }, []);

    const registrar = async (acao: "entrada" | "saida") => {
        if (!placa.trim()) {
            alert("Digite a placa do veículo");
            return;
        }
        setLoading(true);
        try {
            await axios.post(
                `http://localhost:8000/${acao}`,
                { placa },
                { headers: { "X-Usuario-Id": localStorage.getItem("usuario_id") || "" } }
            );
            await fetchStats();
            setPlaca("");
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
                <input
                    type="text"
                    value={placa}
                    onChange={(e) => setPlaca(e.target.value.toUpperCase())}
                    placeholder="Placa do veículo"
                    className="input"
                />
                <button
                    className="btn btn-primary"
                    disabled={loading}
                    onClick={() => registrar("entrada")}
                >
                    Registrar Entrada
                </button>
                <button
                    className="btn btn-secondary"
                    disabled={loading}
                    onClick={() => registrar("saida")}
                >
                    Registrar Saída
                </button>
            </section>
        </div>
    )
}