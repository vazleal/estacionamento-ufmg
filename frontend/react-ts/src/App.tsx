import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import { Home } from "lucide-react";
import { HomePage } from "./pages/HomePage/HomePage";

function App() {
  return (
    <div className="app-wrapper">
      <header className="header">
        <h1>
          Painel de Estacionamento <span>UFMG</span>
        </h1>
      </header>
      <main className="main-content">
        <HomePage />
      </main>
      <footer className="footer">
        <p>Dados atualizados automaticamente a cada 5 segundos</p>
      </footer>
    </div>
  );
}

export default App;
