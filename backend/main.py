# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import estatisticas, configuracoes, entradas
from database import init_db

init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estatisticas.router)
app.include_router(configuracoes.router)
app.include_router(entradas.router)
