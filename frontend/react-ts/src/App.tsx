import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import { HomePage } from "./pages/HomePage/HomePage";
import { LoginPage } from "./pages/LoginPage/LoginPage"; // Importe sua LoginPage

function App() {
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
              <li>
                <Link to="/login" className="btn btn-secondary">Login</Link>
              </li>
            </ul>
          </nav>
        </header>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
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
