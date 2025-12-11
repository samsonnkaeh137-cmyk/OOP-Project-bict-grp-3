from typing import List, Tuple

from repositories.book_repository import BookRepository


class BookService:
    """
    Application/service layer for book catalog operations.

    This is what the PyQt5 UI should talk to, instead of using
    database code directly.
    """

    # Note: we avoid the `BookRepository | None` syntax to remain
    # compatible with Python 3.9 on your system.
    def __init__(self, repo=None):
        self._repo = repo or BookRepository()
        # Ensure table exists once
        self._repo.create_table()

    def add_book(self, title: str, author: str, isbn: str, genre: str, year: str) -> None:
        # Simple validation could go here if needed
        self._repo.add_book(title=title, author=author, isbn=isbn, genre=genre, year=year, quantity=1)

    def update_book(self, book_id: int, title: str, author: str, isbn: str, genre: str, year: str) -> None:
        # For now always set quantity to 1 (no stock logic yet)
        self._repo.update_book(
            book_id=book_id,
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            year=year,
            quantity=1,
        )

    def delete_book(self, book_id: int) -> None:
        self._repo.delete_book(book_id)

    def list_books(self) -> List[Tuple]:
        return self._repo.list_books()

    def search_books(self, keyword: str) -> List[Tuple]:
        return self._repo.search_books(keyword)



