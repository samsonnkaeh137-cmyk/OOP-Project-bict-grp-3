from datetime import datetime, timedelta
from typing import Optional


class Book:
    def __init__(self, id_: int, title: str, author_id: int, isbn: str, genre: str, quantity: int = 1):
        self._id = id_
        self._title = title
        self._author_id = author_id
        self._isbn = isbn
        self._genre = genre
        self._quantity = quantity

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def author_id(self) -> int:
        return self._author_id

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, value: str) -> None:
        self._genre = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = value


class Author:
    def __init__(self, id_: int, name: str):
        self._id = id_
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value


class Role:
    LIBRARIAN = "LIBRARIAN"
    MEMBER = "MEMBER"

    def __init__(self, id_: int, name: str):
        self._id = id_
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class User:
    def __init__(self, id_: int, username: str, password_hash: str, role: Role):
        self._id = id_
        self._username = username
        self._password_hash = password_hash
        self._role = role

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def role(self) -> Role:
        return self._role

    def is_librarian(self) -> bool:
        return self._role.name == Role.LIBRARIAN

    def is_member(self) -> bool:
        return self._role.name == Role.MEMBER


class Member(User):
    def __init__(self, id_: int, username: str, password_hash: str, role: Role, full_name: str):
        super().__init__(id_, username, password_hash, role)
        self._full_name = full_name

    @property
    def full_name(self) -> str:
        return self._full_name


class Librarian(User):
    def __init__(self, id_: int, username: str, password_hash: str, role: Role, employee_id: str):
        super().__init__(id_, username, password_hash, role)
        self._employee_id = employee_id

    @property
    def employee_id(self) -> str:
        return self._employee_id


class BookClub:
    def __init__(self, id_: int, name: str, description: str):
        self._id = id_
        self._name = name
        self._description = description

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description


class Loan:
    def __init__(
        self,
        id_: int,
        book_id: int,
        member_id: int,
        loan_date: datetime,
        due_date: datetime,
        return_date: Optional[datetime] = None,
    ):
        self._id = id_
        self._book_id = book_id
        self._member_id = member_id
        self._loan_date = loan_date
        self._due_date = due_date
        self._return_date = return_date

    @property
    def id(self) -> int:
        return self._id

    @property
    def book_id(self) -> int:
        return self._book_id

    @property
    def member_id(self) -> int:
        return self._member_id

    @property
    def loan_date(self) -> datetime:
        return self._loan_date

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @property
    def return_date(self) -> Optional[datetime]:
        return self._return_date

    @return_date.setter
    def return_date(self, value: datetime) -> None:
        self._return_date = value

    @property
    def is_overdue(self) -> bool:
        if self._return_date is not None:
            return self._return_date > self._due_date
        return datetime.utcnow() > self._due_date

    @staticmethod
    def create_new(book_id: int, member_id: int) -> "Loan":
        loan_date = datetime.utcnow()
        due_date = loan_date + timedelta(days=7)
        # id_ is None here; it will be set when persisted
        return Loan(id_=-1, book_id=book_id, member_id=member_id, loan_date=loan_date, due_date=due_date)



