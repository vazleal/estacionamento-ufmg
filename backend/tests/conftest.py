import pytest
from database import get_connection, init_db, set_db_path

@pytest.fixture(scope="session", autouse=True)
def set_up_test_database():
    set_db_path("tests/testDB.db")
    init_db("tests/testDB.db")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios")
        cursor.execute("DELETE FROM veiculos")
        cursor.execute("DELETE FROM entradas")
        cursor.execute("INSERT INTO usuarios (id, nome, email, senha, matricula, tipo) VALUES (1, 'Admin', 'admin@ex.com', 'admin', '000', 'admin')")
        conn.commit()
    yield
