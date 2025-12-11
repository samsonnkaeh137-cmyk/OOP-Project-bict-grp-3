from typing import List, Optional

from infrastructure.db import connection_scope


class MemberRepository:
    """
    DAO for members.
    """

    def create_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role_id INTEGER NOT NULL REFERENCES roles(id)
        );

        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY REFERENCES users(id),
            full_name TEXT NOT NULL
        );
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def add_member(self, username: str, password_hash: str, role_id: int, full_name: str) -> None:
        sql_user = """
        INSERT INTO users (username, password_hash, role_id)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        sql_member = """
        INSERT INTO members (id, full_name)
        VALUES (%s, %s)
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_user, (username, password_hash, role_id))
                user_id = cur.fetchone()[0]
                cur.execute(sql_member, (user_id, full_name))

    def get_member(self, member_id: int) -> Optional[tuple]:
        sql = """
        SELECT u.id, u.username, m.full_name, u.role_id
        FROM users u
        JOIN members m ON u.id = m.id
        WHERE u.id = %s
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (member_id,))
                return cur.fetchone()

    def list_members(self) -> List[tuple]:
        sql = """
        SELECT u.id, u.username, m.full_name, u.role_id
        FROM users u
        JOIN members m ON u.id = m.id
        ORDER BY u.id
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()



