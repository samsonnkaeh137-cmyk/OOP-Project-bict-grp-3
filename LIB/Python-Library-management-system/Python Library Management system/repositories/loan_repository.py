from typing import List

from infrastructure.db import connection_scope


class LoanRepository:
    """
    DAO for loans.
    """

    def create_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS loans (
            id SERIAL PRIMARY KEY,
            book_id INTEGER NOT NULL REFERENCES books(id),
            member_id INTEGER NOT NULL REFERENCES members(id),
            loan_date TIMESTAMPTZ NOT NULL,
            due_date TIMESTAMPTZ NOT NULL,
            return_date TIMESTAMPTZ
        );
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def count_active_loans_for_member(self, member_id: int) -> int:
        sql = "SELECT COUNT(*) FROM loans WHERE member_id = %s AND return_date IS NULL"
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (member_id,))
                return cur.fetchone()[0]

    def create_loan(self, book_id: int, member_id: int, loan_date, due_date) -> None:
        sql = """
        INSERT INTO loans (book_id, member_id, loan_date, due_date)
        VALUES (%s, %s, %s, %s)
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (book_id, member_id, loan_date, due_date))

    def mark_returned(self, loan_id: int, return_date) -> None:
        sql = "UPDATE loans SET return_date = %s WHERE id = %s"
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (return_date, loan_id))

    def list_loans_for_member(self, member_id: int) -> List[tuple]:
        sql = """
        SELECT id, book_id, member_id, loan_date, due_date, return_date
        FROM loans
        WHERE member_id = %s
        ORDER BY loan_date DESC
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (member_id,))
                return cur.fetchall()

    def get_active_loan_for_member_and_book(self, member_id: int, book_id: int):
        """
        Return the most recent active (not yet returned) loan for this member and book,
        or None if there is no such loan.
        """
        sql = """
        SELECT id
        FROM loans
        WHERE member_id = %s
          AND book_id = %s
          AND return_date IS NULL
        ORDER BY loan_date DESC
        LIMIT 1
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (member_id, book_id))
                return cur.fetchone()



