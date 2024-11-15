import contextlib, sqlite3, pytest

@pytest.fixture
def conn_factory(tmp_path):
    @contextlib.contextmanager
    def open_connection():
        conn = sqlite3.connect(tmp_path / "test.db")
        try:
            yield conn
        finally:
            conn.close()

    return open_connection

def test_some_migration_process_no_commit(conn_factory):
    # Assume the tool is faulty and forgets to commit:
    with conn_factory() as conn:
        conn.execute("CREATE TABLE foo (x)")
        conn.execute("INSERT INTO foo VALUES (123)")
        # conn.commit()

    # Using the same temporary database, we can start a second connection
    # to see that it was never committed:
    with conn_factory() as conn:
        c = conn.execute("SELECT * FROM foo")
        assert c.fetchall() == [(123,)]  # raises AssertionError


def test_some_migration_process_commit(conn_factory):
    # Assume the tool is faulty and forgets to commit:
    with conn_factory() as conn:
        conn.execute("CREATE TABLE foo (x)")
        conn.execute("INSERT INTO foo VALUES (123)")
        conn.commit()

    # Using the same temporary database, we can start a second connection
    # to see that it was never committed:
    with conn_factory() as conn:
        c = conn.execute("SELECT * FROM foo")
        assert c.fetchall() == [(123,)]  # raises AssertionError