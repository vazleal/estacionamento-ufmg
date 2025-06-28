# Integrantes

- Matheus Vaz Leal Lima
- Raphaela Maria Costa e Silva
- Victor Kenji Pawlowski Abeki


# Sistema de Gerenciamento de Vagas - Estacionamento Universitário

Este projeto é um sistema simples para gerenciar o uso de vagas em um estacionamento universitário, com foco em garantir a disponibilidade de vagas para **professores**, utilizando um backend em **FastAPI** e frontend em **React**.

## 🎯 Funcionalidades

- Registro de entrada e saída de veículos de **professores** e **alunos**
- Controle de número total de vagas e vagas reservadas para professores
- Bloqueio automático da entrada de alunos quando o estacionamento estiver cheio
- Alerta quando restarem menos de 10% das vagas reservadas para professores
- Painel de controle em tempo real no frontend
- Persistência das configurações (número de vagas, limite de aviso) no banco de dados

---

## 📦 Tecnologias

### Backend (API):
- [FastAPI](https://fastapi.tiangolo.com/)
- SQLite (via `sqlite3`)
- Estrutura modular com rotas separadas

### Frontend:
- [React](https://react.dev/) com Vite + TypeScript
- Integração com a API via `axios`
- Atualização em tempo real com `useEffect`

---

## 🚀 Como executar o projeto

### 🔧 Requisitos
- Python 3.9+
- Node.js 18+

### ⚙️ Backend
```bash
# Entrar no backend
cd backend

# Instalar dependências
pip install -r requirements.txt

# Rodar
uvicorn main:app --reload

# Rodar no windows
python -m uvicorn main:app --reload
```

### 🖥️ Frontend
```bash
cd frontend/react-ts
npm install

# Rodar
npm run dev

```

---

## 📁 Estrutura do Projeto

```bash
estacionamento-ufmg/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── estatisticas.py
│   │   ├── configuracoes.py
│   │   ├── entradas.py
│   │   └── usuarios.py
│   ├── tests/...
│   ├── data/
│   │   └── estacionamento.db
├── frontend/
│   └── react-ts/
│       └── src/
│           ├── App.tsx
│           ├── main.tsx
│           └── pages/...
│           └── __tests__/...
```