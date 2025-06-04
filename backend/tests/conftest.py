import pytest
from database import get_connection, init_db, set_db_path


@pytest.fixture(scope="session", autouse=True)
def set_up_test_database():
    set_db_path("tests/testDB.db")
    init_db("tests/testDB.db")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
    yield