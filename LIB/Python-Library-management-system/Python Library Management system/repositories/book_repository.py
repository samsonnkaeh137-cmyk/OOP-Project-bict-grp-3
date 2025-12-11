from typing import List, Optional

from infrastructure.db import connection_scope


class BookRepository:
    """
    DAO for books. Implements CRUD using psycopg2.

    Schema kept close to the existing UI:
      - id, title, author, isbn, genre, year, quantity
    """

    def create_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL,
            genre TEXT NOT NULL,
            year TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1
        );
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def add_book(
        self,
        title: str,
        author: str,
        isbn: str,
        genre: str,
        year: str,
        quantity: int = 1,
    ) -> None:
        sql = """
        INSERT INTO books (title, author, isbn, genre, year, quantity)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (title, author, isbn, genre, year, quantity))

    def update_book(
        self,
        book_id: int,
        title: str,
        author: str,
        isbn: str,
        genre: str,
        year: str,
        quantity: int,
    ) -> None:
        sql = """
        UPDATE books
        SET title = %s,
            author = %s,
            isbn = %s,
            genre = %s,
            year = %s,
            quantity = %s
        WHERE id = %s
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (title, author, isbn, genre, year, quantity, book_id))

    def delete_book(self, book_id: int) -> None:
        sql = "DELETE FROM books WHERE id = %s"
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (book_id,))

    def get_book(self, book_id: int) -> Optional[tuple]:
        sql = """
        SELECT id, title, author, isbn, genre, year, quantity
        FROM books
        WHERE id = %s
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (book_id,))
                return cur.fetchone()

    def list_books(self) -> List[tuple]:
        sql = """
        SELECT id, title, author, isbn, genre, year, quantity
        FROM books
        ORDER BY id
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def search_books(self, keyword: str) -> List[tuple]:
        sql = """
        SELECT id, title, author, isbn, genre, year, quantity
        FROM books
        WHERE title ILIKE %s
           OR author ILIKE %s
           OR isbn ILIKE %s
           OR genre ILIKE %s
        ORDER BY id
        """
        pattern = f"%{keyword}%"
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (pattern, pattern, pattern, pattern))
                return cur.fetchall()



