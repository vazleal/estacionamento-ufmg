import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import { HomePage } from "./pages/HomePage/HomePage";
import { LoginPage } from "./pages/LoginPage/LoginPage";
import { UserPanelPage } from "./pages/UserPanelPage/UserPanelPage";

function App() {

  const isLoggedIn = !!localStorage.getItem("usuario_id");


  return (
    <Router>
      <div className="app-wrapper">
        <header className="header">
          <h1 className="header-title">
            Painel de Estacionamento <span>UFMG</span>
          </h1>
          <nav className="nav">
            <ul>
              <li>
                <Link to="/" className="btn btn-secondary">Home</Link>
              </li>
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
            <Route path="/" element={<HomePage />} />
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
