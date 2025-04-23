import { useEffect, useState } from "react";
import axios from "axios";

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
    const res = await axios.get<Estatisticas>("http://localhost:8000/estatisticas");
    setStats(res.data);
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const registrar = async (tipo: "professor" | "aluno", acao: "entrada" | "saida") => {
    setLoading(true);
    try {
      await axios.post(`http://localhost:8000/${acao}/${tipo}`);
      await fetchStats();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Erro ao registrar ação");
    } finally {
      setLoading(false);
    }
  };

  if (!stats) return <div>Carregando...</div>;

  return (
    <div style={{ padding: "2rem", maxWidth: 800, margin: "0 auto" }}>
      <h1>Painel de Estacionamento</h1>
      <p>Total de Vagas: {stats.total}</p>
      <p>Reservadas para Professores: {stats.reservadas_prof}</p>
      <p>Ocupadas: {stats.ocupadas}</p>
      <p>Professores: {stats.professores}</p>
      <p>Alunos: {stats.alunos}</p>
      <p>Livres: {stats.livres}</p>
      <p>Livres para Professores: {stats.livres_prof}</p>
      {stats.alerta && (
        <p style={{ color: "orange", fontWeight: "bold" }}>
          ⚠️ Atenção: poucas vagas reservadas para professores!
        </p>
      )}
      {stats.bloquear_aluno && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          🚫 Entrada de alunos temporariamente bloqueada.
        </p>
      )}

      <div style={{ marginTop: "1rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <button disabled={loading} onClick={() => registrar("professor", "entrada")}>+ Professor</button>
        <button disabled={loading || stats.bloquear_aluno} onClick={() => registrar("aluno", "entrada")}>+ Aluno</button>
        <button disabled={loading} onClick={() => registrar("professor", "saida")}>- Professor</button>
        <button disabled={loading} onClick={() => registrar("aluno", "saida")}>- Aluno</button>
      </div>
    </div>
  );
}

export default App;
