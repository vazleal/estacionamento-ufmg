import React, { useState, useEffect, ChangeEvent, FormEvent } from "react";
import "../../App.css";
import "./UserPanelPage.css";

interface Veiculo {
  id: number;
  placa: string;
}

const API_BASE_URL = "http://localhost:8000"; 

export const UserPanelPage: React.FC = () => {
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [novaPlaca, setNovaPlaca] = useState<string>("");
  const [editingVeiculo, setEditingVeiculo] = useState<Veiculo | null>(null);
  const [editingPlaca, setEditingPlaca] = useState<string>(""); 

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const usuarioId = localStorage.getItem("usuario_id");
  const usuarioNome = localStorage.getItem("usuario_nome");

  const clearMessages = () => {
    setError(null);
    setSuccessMessage(null);
  };

  const displayError = (message: string) => {
    setSuccessMessage(null);
    setError(message);
    setTimeout(clearMessages, 5000);
  }

  const displaySuccess = (message: string) => {
    setError(null);
    setSuccessMessage(message);
    setTimeout(clearMessages, 3000);
  }

  // Buscar veículos do usuário
  const fetchVeiculos = async () => {
    if (!usuarioId) return;
    setIsLoading(true);
    clearMessages();
    try {
      const response = await fetch(
        `${API_BASE_URL}/usuario/${usuarioId}/veiculos`,
        { headers: { "X-Usuario-Id": usuarioId } }
      );
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({detail: "Falha ao buscar veículos."}));
        throw new Error(errorData.detail);
      }
      const data: Veiculo[] = await response.json();
      setVeiculos(data);
    } catch (err: any) {
      console.error("Erro ao buscar veículos:", err);
      displayError(err.message || "Ocorreu um erro ao buscar seus veículos.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const tipo = localStorage.getItem("usuario_tipo");
    if (!usuarioId) {
      window.location.href = "/login";
      return;
    }
    if (tipo === "admin") {
      window.location.href = "/estacionamento";
      return;
    }
    fetchVeiculos();
  }, [usuarioId]);

  const formatPlaca = (v: string) => v.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 7);

  const handleNovaPlacaChange = (e: ChangeEvent<HTMLInputElement>) => {
    setNovaPlaca(formatPlaca(e.target.value));
  };

  // Adicionar Veículo
  const handleAddVeiculo = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!novaPlaca.trim()) {
      displayError("A placa não pode estar vazia.");
      return;
    }
    if (!usuarioId) return;

    setIsLoading(true);
    clearMessages();
    try {
      const response = await fetch(
        `${API_BASE_URL}/usuario/${usuarioId}/veiculos`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Usuario-Id": usuarioId,
          },
          body: JSON.stringify({ placa: novaPlaca }),
        }
      );
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({detail: "Falha ao adicionar veículo."}));
        throw new Error(errorData.detail);
      }
      // const novoVeiculoAdicionado: Veiculo = await response.json();
      setNovaPlaca("");
      fetchVeiculos();
      displaySuccess("Veículo adicionado com sucesso! 🚗");
    } catch (err: any) {
      console.error("Erro ao adicionar veículo:", err);
      displayError(err.message || "Ocorreu um erro ao adicionar. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteVeiculo = async (veiculoId: number) => {
    if (!usuarioId) return;
    if (!window.confirm("Tem certeza que deseja remover este veículo?")) return;

    setIsLoading(true);
    clearMessages();
    try {
      const response = await fetch(
        `${API_BASE_URL}/usuario/${usuarioId}/veiculos/${veiculoId}`,
        {
          method: "DELETE",
          headers: { "X-Usuario-Id": usuarioId },
        }
      );
      if (!response.ok && response.status !== 204) {
        const errorData = await response.json().catch(() => ({detail: "Falha ao remover veículo."}));
        throw new Error(errorData.detail);
      }
      fetchVeiculos();
      displaySuccess("Veículo removido com sucesso! 🗑️");
    } catch (err: any) {
      console.error("Erro ao remover veículo:", err);
      displayError(err.message || "Ocorreu um erro ao remover. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  // Iniciar Edição
  const handleStartEditVeiculo = (veiculo: Veiculo) => {
    setEditingVeiculo(veiculo);
    setEditingPlaca(veiculo.placa);
    clearMessages();
  };

  // Cancelar Edição
  const handleCancelEdit = () => {
    setEditingVeiculo(null);
    setEditingPlaca("");
    clearMessages();
  };

  const handleEditingPlacaChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEditingPlaca(formatPlaca(e.target.value));
  };

  // Atualizar Veículo
  const handleUpdateVeiculo = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!editingVeiculo || !editingPlaca.trim()) {
      displayError("Placa de edição não pode estar vazia.");
      return;
    }
    if (!usuarioId) return;

    setIsLoading(true);
    clearMessages();
    try {
      const response = await fetch(
        `${API_BASE_URL}/usuario/${usuarioId}/veiculos/${editingVeiculo.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-Usuario-Id": usuarioId,
          },
          body: JSON.stringify({ placa: editingPlaca }),
        }
      );
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({detail: "Falha ao atualizar veículo."}));
        throw new Error(errorData.detail);
      }
      // const veiculoAtualizado: Veiculo = await response.json();
      setEditingVeiculo(null);
      setEditingPlaca("");
      fetchVeiculos();
      displaySuccess("Veículo atualizado com sucesso! 🛠️");
    } catch (err: any) {
      console.error("Erro ao atualizar veículo:", err);
      displayError(err.message || "Ocorreu um erro ao atualizar. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  if (!usuarioId) {
    return <p>Redirecionando para login...</p>;
  }

  return (
    <main className="main-content">
      <div className="login-card user-panel-card">
        <h2>Painel do Usuário</h2>
        <p>Bem-vindo(a) ao seu painel, <strong>{usuarioNome || "Usuário"}</strong>!</p>

        {isLoading && <p className="loading-message">Processando...</p>}
        {error && <p className="error-message">{error}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        {/* Seção de Gerenciamento de Veículos */}
        <div className="veiculos-manager">
          <h3>Gerenciar Veículos</h3>

          {/* Formulário para ADICIONAR ou EDITAR veículo */}
          {editingVeiculo ? (
            <form onSubmit={handleUpdateVeiculo} className="veiculo-form veiculo-edit-form">
              <h4>Editando Veículo: <span className="placa-original">{editingVeiculo.placa}</span></h4>
              <div className="form-group">
                <label htmlFor="editingPlaca">Nova Placa:</label>
                <input
                  type="text"
                  id="editingPlaca"
                  value={editingPlaca}
                  onChange={handleEditingPlacaChange}
                  placeholder="ABC1234"
                  maxLength={7}
                  required
                  className="veiculo-input"
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn btn-save" disabled={isLoading}>
                  {isLoading ? "Salvando..." : "Salvar Alterações"}
                </button>
                <button type="button" onClick={handleCancelEdit} className="btn btn-cancel" disabled={isLoading}>
                  Cancelar
                </button>
              </div>
            </form>
          ) : (
            <form onSubmit={handleAddVeiculo} className="veiculo-form veiculo-add-form">
              <h4>Adicionar Novo Veículo</h4>
              <div className="form-group">
                <label htmlFor="novaPlaca">Placa do Veículo:</label>
                <input
                  type="text"
                  id="novaPlaca"
                  value={novaPlaca}
                  onChange={handleNovaPlacaChange}
                  placeholder="ABC1234"
                  maxLength={7}
                  required
                  className="veiculo-input"
                />
              </div>
              <button type="submit" className="btn btn-add" disabled={isLoading}>
                {isLoading ? "Adicionando..." : "Adicionar Veículo"}
              </button>
            </form>
          )}

          {/* Lista de veículos */}
          <h4>Seus Veículos Cadastrados</h4>
          {veiculos.length === 0 && !isLoading && (
            <p>Você ainda não cadastrou nenhum veículo.</p>
          )}
          {veiculos.length > 0 && (
            <ul className="veiculos-list">
              {veiculos.map((veiculo) => (
                <li key={veiculo.id} className="veiculo-item">
                  <span className="veiculo-placa">{veiculo.placa}</span>
                  <div className="veiculo-actions">
                    <button
                      onClick={() => handleStartEditVeiculo(veiculo)}
                      className="btn btn-edit"
                      title="Editar Veículo"
                      disabled={isLoading || !!editingVeiculo}
                    >
                      ✏️ Editar
                    </button>
                    <button
                      onClick={() => handleDeleteVeiculo(veiculo.id)}
                      className="btn btn-remove"
                      title="Remover Veículo"
                      disabled={isLoading || !!editingVeiculo}
                    >
                      🗑️ Remover
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </main>
  );
};

export default UserPanelPage;