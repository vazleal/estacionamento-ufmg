import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import "./App.css";
import { EstacionamentoPage } from "./pages/EstacionamentoPage/EstacionamentoPage";
import { LoginPage } from "./pages/LoginPage/LoginPage";
import { UserPanelPage } from "./pages/UserPanelPage/UserPanelPage";
import { useState } from "react";

function App() {
  const [isLoggedIn] = useState<boolean>(!!localStorage.getItem("usuario_id"));
  const usuarioTipo = localStorage.getItem("usuario_tipo");

  return (
    <Router>
      <div className="app-wrapper">
        <header className="header">
          <h1 className="header-title">
            Painel de Estacionamento <span>UFMG</span>
          </h1>
          <nav className="nav">
            <ul>
              {usuarioTipo === "admin" && (
                <li>
                  <Link to="/estacionamento" className="btn btn-secondary">Estacionamento</Link>
                </li>
              )}
              {!isLoggedIn ? (
                <li>
                  <Link to="/login" className="btn btn-secondary">Login</Link>
                </li>
              ) : (
                <li >
                  <Link to="/painel" className="btn btn-secondary">Painel</Link>
                </li>
              )}
            </ul>
          </nav>
        </header>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/estacionamento" replace />} />
            <Route path="/estacionamento" element={<EstacionamentoPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/painel" element={<UserPanelPage />} />
          </Routes>
        </main>
        <footer className="footer">
          <p>Dados atualizados automaticamente a cada 5 segundos</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
