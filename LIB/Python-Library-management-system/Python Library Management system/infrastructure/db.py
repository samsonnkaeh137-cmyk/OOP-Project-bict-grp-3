import os
from contextlib import contextmanager
from typing import Dict, Any

import psycopg2


def _get_connection_params() -> Dict[str, Any]:
    """
    Central place for PostgreSQL connection configuration.

    All connection parameters must be provided via environment variables:
      - LIB_DB_NAME     (required)
      - LIB_DB_USER     (required)
      - LIB_DB_PASSWORD (required) - NEVER hardcode this value
      - LIB_DB_HOST     (default: localhost)
      - LIB_DB_PORT     (default: 5432)

    Raises ValueError if required environment variables are not set.
    """
    dbname = os.getenv("LIB_DB_NAME")
    user = os.getenv("LIB_DB_USER")
    password = os.getenv("LIB_DB_PASSWORD")
    
    if not dbname:
        raise ValueError("LIB_DB_NAME environment variable is required")
    if not user:
        raise ValueError("LIB_DB_USER environment variable is required")
    if not password:
        raise ValueError("LIB_DB_PASSWORD environment variable is required (never hardcode passwords)")
    
    port_str = os.getenv("LIB_DB_PORT", "5432")
    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"LIB_DB_PORT must be a valid integer, got: {port_str}")
    
    return {
        "dbname": dbname,
        "user": user,
        "password": password,
        "host": os.getenv("LIB_DB_HOST", "localhost"),
        "port": port,
    }


def get_connection():
    """
    Return a new psycopg2 connection.
    Callers are responsible for closing it, or use connection_scope.
    """
    # pyright: ignore[reportGeneralTypeIssues]
    return psycopg2.connect(**_get_connection_params())


@contextmanager
def connection_scope():
    """
    Context manager that opens a connection and commits/rolls back safely.
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()



