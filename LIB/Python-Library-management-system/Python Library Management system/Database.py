import os

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    """
    PostgreSQL-backed database for the library app.

    Connection settings must be provided via environment variables:
      - LIB_DB_NAME     (required)
      - LIB_DB_USER     (required)
      - LIB_DB_PASSWORD (required) - NEVER hardcode this value
      - LIB_DB_HOST     (default: localhost)
      - LIB_DB_PORT     (default: 5432)

    Raises ValueError if required environment variables are not set.

    We keep the db_name parameter for compatibility with existing code
    (it is ignored when using PostgreSQL).
    """

    def __init__(self, db_name=None):
        dbname = os.getenv("LIB_DB_NAME")
        user = os.getenv("LIB_DB_USER")
        password = os.getenv("LIB_DB_PASSWORD")
        
        if not dbname:
            raise ValueError("LIB_DB_NAME environment variable is required")
        if not user:
            raise ValueError("LIB_DB_USER environment variable is required")
        if not password:
            raise ValueError("LIB_DB_PASSWORD environment variable is required (never hardcode passwords)")
        
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=os.getenv("LIB_DB_HOST", "localhost"),
            port=os.getenv("LIB_DB_PORT", "5432"),
        )
        self.connection.autocommit = True
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL,
            genre TEXT NOT NULL,
            year TEXT NOT NULL
        )
        """
        with self.connection.cursor() as cur:
            cur.execute(query)

    def add_book(self, title, author, isbn, genre, year):
        query = """
        INSERT INTO books (title, author, isbn, genre, year)
        VALUES (%s, %s, %s, %s, %s)
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (title, author, isbn, genre, year))

    def update_book(self, book_id, title, author, isbn, genre, year):
        query = """
        UPDATE books
        SET title = %s, author = %s, isbn = %s, genre = %s, year = %s
        WHERE id = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (title, author, isbn, genre, year, book_id))

    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE id = %s"
        with self.connection.cursor() as cur:
            cur.execute(query, (book_id,))

    def get_books(self):
        query = "SELECT id, title, author, isbn, genre, year FROM books ORDER BY id"
        with self.connection.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_book_by_id(self, book_id):
        query = "SELECT id, title, author, isbn, genre, year FROM books WHERE id = %s"
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (book_id,))
            return cur.fetchone()

    def search_books(self, keyword):
        query = """
        SELECT id, title, author, isbn, genre, year
        FROM books
        WHERE title ILIKE %s
           OR author ILIKE %s
           OR isbn ILIKE %s
           OR genre ILIKE %s
        ORDER BY id
        """
        wildcard_keyword = f"%{keyword}%"
        with self.connection.cursor() as cur:
            cur.execute(
                query,
                (wildcard_keyword, wildcard_keyword, wildcard_keyword, wildcard_keyword),
            )
            return cur.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()
