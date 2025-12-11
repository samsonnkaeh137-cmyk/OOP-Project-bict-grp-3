import hashlib
from typing import Optional, Tuple

from repositories.member_repository import MemberRepository
from infrastructure.db import connection_scope


def _hash_password(raw: str) -> str:
    # Simple demo hash, not for production use
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class AuthService:
    """
    Handles user/role setup and login.
    """

    # Avoid `MemberRepository | None` so it's compatible with Python 3.9.
    def __init__(self, member_repo=None):
        self._repo = member_repo or MemberRepository()
        self._repo.create_table()
        self._ensure_default_roles_and_users()

    def _ensure_default_roles_and_users(self) -> None:
        """
        Insert default roles and demo users if they do not exist:
          - Role: LIBRARIAN, MEMBER
          - Users:
              librarian / admin123  (LIBRARIAN)
              member    / member123 (MEMBER)
        """
        with connection_scope() as conn:
            with conn.cursor() as cur:
                # Ensure roles
                cur.execute(
                    "INSERT INTO roles (name) VALUES ('LIBRARIAN') "
                    "ON CONFLICT (name) DO NOTHING"
                )
                cur.execute(
                    "INSERT INTO roles (name) VALUES ('MEMBER') "
                    "ON CONFLICT (name) DO NOTHING"
                )

                # Get role ids
                cur.execute("SELECT id, name FROM roles")
                roles = {name: rid for rid, name in cur.fetchall()}
                librarian_role_id = roles.get("LIBRARIAN")
                member_role_id = roles.get("MEMBER")

                # Ensure demo users
                cur.execute("SELECT username FROM users WHERE username = %s", ("librarian",))
                if cur.fetchone() is None:
                    cur.execute(
                        """
                        INSERT INTO users (username, password_hash, role_id)
                        VALUES (%s, %s, %s)
                        RETURNING id
                        """,
                        ("librarian", _hash_password("admin123"), librarian_role_id),
                    )
                    librarian_id = cur.fetchone()[0]
                    cur.execute(
                        "INSERT INTO members (id, full_name) VALUES (%s, %s)",
                        (librarian_id, "Head Librarian"),
                    )

                cur.execute("SELECT username FROM users WHERE username = %s", ("member",))
                if cur.fetchone() is None:
                    cur.execute(
                        """
                        INSERT INTO users (username, password_hash, role_id)
                        VALUES (%s, %s, %s)
                        RETURNING id
                        """,
                        ("member", _hash_password("member123"), member_role_id),
                    )
                    member_id = cur.fetchone()[0]
                    cur.execute(
                        "INSERT INTO members (id, full_name) VALUES (%s, %s)",
                        (member_id, "Regular Member"),
                    )

    def login(self, username: str, password: str) -> Optional[Tuple[int, str]]:
        """
        Returns (user_id, role_name) on success, or None on failure.
        """
        password_hash = _hash_password(password)
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.id, r.name
                    FROM users u
                    JOIN roles r ON u.role_id = r.id
                    WHERE u.username = %s AND u.password_hash = %s
                    """,
                    (username, password_hash),
                )
                row = cur.fetchone()
                if row:
                    return row[0], row[1]
        return None



