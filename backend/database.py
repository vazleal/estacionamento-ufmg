# database.py
import sqlite3
import os

DATABASE = 'data/estacionamento.db'

def init_db():
    if not os.path.exists('data'):
        os.makedirs('data')
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entradas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                data_hora TEXT NOT NULL,
                dia_semana TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                total_vagas INTEGER NOT NULL,
                reservadas_professores INTEGER NOT NULL,
                aviso_limite REAL NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO configuracoes (id, total_vagas, reservadas_professores, aviso_limite)
            VALUES (1, 100, 40, 0.1)
        ''')
        conn.commit()

def get_connection():
    return sqlite3.connect(DATABASE)
