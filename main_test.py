from unittest.mock import MagicMock

import psycopg2.pool
import sqlalchemy



def test_main_postgressql():
    import main_postgres
    main_postgres.psycopg2.connect = MagicMock()
    mock_cursor = main_postgres.psycopg2.connect().cursor()
    mock_cursor.__enter__().fetchall.return_value = [['0']]

    main_postgres.app.testing = True
    client = main_postgres.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '0' in r.data.decode('utf-8')


def test_main_postgressql_pooling():
    psycopg2.pool.ThreadedConnectionPool = MagicMock()

    import main_postgres_pooling

    mock_pool = main_postgres_pooling.psycopg2.pool.ThreadedConnectionPool()
    mock_pool.getconn().cursor().__enter__().fetchall.return_value = [['0']]

    main_postgres_pooling.app.testing = True
    client = main_postgres_pooling.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '0' in r.data.decode('utf-8')