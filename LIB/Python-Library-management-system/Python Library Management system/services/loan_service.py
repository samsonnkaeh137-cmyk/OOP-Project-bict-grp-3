from datetime import datetime, timedelta

from repositories.book_repository import BookRepository
from repositories.loan_repository import LoanRepository


class LoanService:
    """
    Service layer for loan workflows.

    Business rules:
      - Max 3 active loans per member.
      - Loan due date is 7 days from loan_date.
    """

    MAX_ACTIVE_LOANS_PER_MEMBER = 3
    LOAN_DAYS = 7

    def __init__(self, book_repo: BookRepository, loan_repo: LoanRepository):
        self._book_repo = book_repo
        self._loan_repo = loan_repo

    def borrow_book(self, member_id: int, book_id: int) -> None:
        active_loans = self._loan_repo.count_active_loans_for_member(member_id)
        if active_loans >= self.MAX_ACTIVE_LOANS_PER_MEMBER:
            raise ValueError("Member has reached the maximum number of active loans.")

        # In a fuller implementation we would also check that quantity > 0 and decrement it.
        loan_date = datetime.utcnow()
        due_date = loan_date + timedelta(days=self.LOAN_DAYS)
        self._loan_repo.create_loan(book_id=book_id, member_id=member_id, loan_date=loan_date, due_date=due_date)

    def return_book(self, loan_id: int) -> None:
        return_date = datetime.utcnow()
        self._loan_repo.mark_returned(loan_id=loan_id, return_date=return_date)

    def return_book_for_member_and_book(self, member_id: int, book_id: int) -> None:
        """
        Convenience method for the UI: finds the active loan for this
        member + book and marks it as returned.
        """
        row = self._loan_repo.get_active_loan_for_member_and_book(member_id, book_id)
        if row is None:
            raise ValueError("No active loan found for this book and member.")
        loan_id = row[0]
        self.return_book(loan_id)



