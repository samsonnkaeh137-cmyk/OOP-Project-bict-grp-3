import sys
import os
# pyright: reportMissingImports=false

# Set database environment variables if not already set
if not os.getenv("LIB_DB_NAME"):
    os.environ['LIB_DB_NAME'] = 'library'
if not os.getenv("LIB_DB_USER"):
    os.environ['LIB_DB_USER'] = 'postgres'
if not os.getenv("LIB_DB_PASSWORD"):
    os.environ['LIB_DB_PASSWORD'] = 'samson'
if not os.getenv("LIB_DB_HOST"):
    os.environ['LIB_DB_HOST'] = 'localhost'
if not os.getenv("LIB_DB_PORT"):
    # Try port 5433 first (common alternative), then 5432
    os.environ['LIB_DB_PORT'] = '5433'

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QLabel, QGroupBox, QGridLayout, QInputDialog
from PyQt5.QtCore import Qt

from services.book_service import BookService
from services.loan_service import LoanService
from repositories.book_repository import BookRepository
from repositories.loan_repository import LoanRepository


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        try:
            # Use the clean architecture services instead of direct DB access
            self.book_service = BookService()

            # Loan service with PostgreSQL-backed repositories
            book_repo = BookRepository()
            loan_repo = LoanRepository()
            loan_repo.create_table()
            self.loan_service = LoanService(book_repo, loan_repo)
            self.init_ui()
        except Exception as e:
            error_msg = str(e)
            if "password authentication failed" in error_msg.lower():
                detailed_msg = (
                    f"PostgreSQL password authentication failed.\n\n"
                    f"Current settings:\n"
                    f"  Database: {os.getenv('LIB_DB_NAME')}\n"
                    f"  User: {os.getenv('LIB_DB_USER')}\n"
                    f"  Host: {os.getenv('LIB_DB_HOST')}\n"
                    f"  Port: {os.getenv('LIB_DB_PORT')}\n\n"
                    f"Please update the password in the code (line 11-12) or set the "
                    f"LIB_DB_PASSWORD environment variable with your PostgreSQL password."
                )
            else:
                detailed_msg = f"Failed to initialize application:\n{str(e)}"
            
            QMessageBox.critical(None, "Initialization Error", detailed_msg)
            raise

    def init_ui(self):
        self.setWindowTitle('LUCT Library Management System')
        self.setGeometry(100, 50, 1600, 900)

        # Yellow and black theme
        self.setStyleSheet(
            """
            QWidget {
                background-color: #000000;
                color: #ffd700;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
            }
            QLabel {
                color: #ffd700;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #1a1a1a;
                color: #ffd700;
                border: 2px solid #ffd700;
                padding: 10px;
                border-radius: 8px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #ffff00;
                background-color: #2a2a2a;
            }
            QPushButton {
                background-color: #ffd700;
                color: #000000;
                border: 2px solid #ffd700;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #ffff00;
                border: 2px solid #ffff00;
            }
            QPushButton:pressed {
                background-color: #ffed4e;
                border: 2px solid #ffed4e;
            }
            QPushButton#danger {
                background-color: #ff4444;
                color: #ffffff;
                border: 2px solid #ff4444;
            }
            QPushButton#danger:hover {
                background-color: #ff6666;
                border: 2px solid #ff6666;
            }
            QPushButton#success {
                background-color: #44ff44;
                color: #000000;
                border: 2px solid #44ff44;
            }
            QPushButton#success:hover {
                background-color: #66ff66;
                border: 2px solid #66ff66;
            }
            QPushButton#warning {
                background-color: #ffd700;
                color: #000000;
                border: 2px solid #ffd700;
            }
            QPushButton#warning:hover {
                background-color: #ffff00;
                border: 2px solid #ffff00;
            }
            QTableWidget {
                background-color: #1a1a1a;
                color: #ffd700;
                gridline-color: #333333;
                border: 2px solid #ffd700;
                border-radius: 10px;
                selection-background-color: #ffd700;
                selection-color: #000000;
                alternate-background-color: #2a2a2a;
            }
            QHeaderView::section {
                background-color: #ffd700;
                color: #000000;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 11pt;
            }
            QGroupBox {
                border: 2px solid #ffd700;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                background-color: rgba(26, 26, 26, 0.8);
                color: #ffd700;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: #ffd700;
                font-size: 13pt;
            }
            """
        )

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Header with yellow and black theme
        header_label = QLabel('📚 LUCT LIBRARY MANAGEMENT SYSTEM', self)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 32pt;
                font-weight: bold;
                color: #000000;
                padding: 15px;
                background-color: #ffd700;
                border-radius: 15px;
            }
        """)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Top section: Search and Quick Actions
        top_section = QHBoxLayout()
        top_section.setSpacing(15)
        
        # Search Group - Left side
        search_group = QGroupBox("🔍 Search Books", self)
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Search by Title, Author, ISBN, or Genre...')
        self.search_input.returnPressed.connect(self.search_books)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_button)
        
        search_group.setLayout(search_layout)
        top_section.addWidget(search_group, 2)
        
        # Quick Actions - Right side
        quick_actions = QGroupBox("⚡ Quick Actions", self)
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(10)
        
        self.View_button = QPushButton('View All', self)
        self.View_button.clicked.connect(self.View_books)
        quick_layout.addWidget(self.View_button)
        
        self.borrow_button = QPushButton('Borrow', self)
        self.borrow_button.setObjectName("warning")
        self.borrow_button.clicked.connect(self.borrow_selected_book)
        quick_layout.addWidget(self.borrow_button)
        
        self.return_button = QPushButton('Return', self)
        self.return_button.setObjectName("warning")
        self.return_button.clicked.connect(self.return_selected_book)
        quick_layout.addWidget(self.return_button)
        
        quick_actions.setLayout(quick_layout)
        top_section.addWidget(quick_actions, 1)
        
        main_layout.addLayout(top_section)

        # Table to display books - Larger and prominent
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'ISBN', 'Genre', 'Year'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(350)
        main_layout.addWidget(self.table, 1)

        # Bottom section: Book Management
        bottom_section = QHBoxLayout()
        bottom_section.setSpacing(15)
        
        # Book Information Group - Left
        book_info_group = QGroupBox("📖 Book Information", self)
        book_info_layout = QGridLayout()
        book_info_layout.setSpacing(12)
        book_info_layout.setContentsMargins(15, 20, 15, 15)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Book title')
        book_info_layout.addWidget(QLabel('Title:'), 0, 0)
        book_info_layout.addWidget(self.title_input, 0, 1)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText('Author name')
        book_info_layout.addWidget(QLabel('Author:'), 0, 2)
        book_info_layout.addWidget(self.author_input, 0, 3)

        self.isbn_input = QLineEdit(self)
        self.isbn_input.setPlaceholderText('ISBN')
        book_info_layout.addWidget(QLabel('ISBN:'), 1, 0)
        book_info_layout.addWidget(self.isbn_input, 1, 1)

        self.genre_input = QLineEdit(self)
        self.genre_input.setPlaceholderText('Genre')
        book_info_layout.addWidget(QLabel('Genre:'), 1, 2)
        book_info_layout.addWidget(self.genre_input, 1, 3)

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText('Publication year')
        book_info_layout.addWidget(QLabel('Year:'), 2, 0)
        book_info_layout.addWidget(self.year_input, 2, 1)

        book_info_group.setLayout(book_info_layout)
        bottom_section.addWidget(book_info_group, 2)

        # Management Actions - Right
        actions_group = QGroupBox("🛠️ Management", self)
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(12)

        self.add_button = QPushButton('➕ Add Book', self)
        self.add_button.setObjectName("success")
        self.add_button.clicked.connect(self.add_book)
        actions_layout.addWidget(self.add_button)

        self.update_button = QPushButton('✏️ Update Book', self)
        self.update_button.clicked.connect(self.update_book)
        actions_layout.addWidget(self.update_button)

        self.delete_button = QPushButton('🗑️ Delete Book', self)
        self.delete_button.setObjectName("danger")
        self.delete_button.clicked.connect(self.delete_book)
        actions_layout.addWidget(self.delete_button)

        actions_group.setLayout(actions_layout)
        bottom_section.addWidget(actions_group, 1)
        
        main_layout.addLayout(bottom_section)

        self.setLayout(main_layout)
        self.View_books()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        genre = self.genre_input.text()
        year = self.year_input.text()

        # Check if fields are filled
        if title and author and isbn and genre and year:
            try:
                self.book_service.add_book(title, author, isbn, genre, year)
                QMessageBox.information(self, 'Success', 'Book added successfully!')
                self.View_books()  # Refresh the table with updated data
                # Clear input fields
                self.title_input.clear()
                self.author_input.clear()
                self.isbn_input.clear()
                self.genre_input.clear()
                self.year_input.clear()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to add book: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'All fields are required!')

    def update_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id_item = self.table.item(selected_row, 0)
            if book_id_item is None:
                QMessageBox.warning(self, 'Error', 'No book selected for update!')
                return

            book_id = int(book_id_item.text())
            title = self.title_input.text()
            author = self.author_input.text()
            isbn = self.isbn_input.text()
            genre = self.genre_input.text()
            year = self.year_input.text()

            # Use current table data if fields are empty
            def cell_text(row, col):
                item = self.table.item(row, col)
                return item.text() if item else ""

            title = title if title else cell_text(selected_row, 1)
            author = author if author else cell_text(selected_row, 2)
            isbn = isbn if isbn else cell_text(selected_row, 3)
            genre = genre if genre else cell_text(selected_row, 4)
            year = year if year else cell_text(selected_row, 5)

            try:
                self.book_service.update_book(book_id, title, author, isbn, genre, year)
                QMessageBox.information(self, 'Success', 'Book updated successfully!')
                self.View_books()  # Refresh the table with updated data
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update book: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'No book selected for update!')

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id_item = self.table.item(selected_row, 0)
            if book_id_item is None:
                QMessageBox.warning(self, 'Error', 'Invalid selection.')
                return

            book_id = int(book_id_item.text())
            confirmation = QMessageBox.question(self, 'Confirm Deletion',
                                                f'Are you sure you want to delete book ID {book_id}?',
                                                QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.book_service.delete_book(book_id)
                QMessageBox.information(self, 'Success', 'Book deleted successfully!')
                self.table.removeRow(selected_row)  # Remove the row from table view
        else:
            QMessageBox.warning(self, 'Error', 'No book selected for deletion!')

    def View_books(self):
        try:
            self.table.setRowCount(0)
            books = self.book_service.list_books()
            for book in books:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for column, data in enumerate(book):
                    self.table.setItem(row_position, column, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load books:\n{str(e)}")
            # Still show empty table so window is usable

    def search_books(self):
        keyword = self.search_input.text()
        books = self.book_service.search_books(keyword)
        self.table.setRowCount(0)
        for book in books:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(book):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def borrow_selected_book(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a book to borrow.")
            return

        book_id_item = self.table.item(selected_row, 0)
        if book_id_item is None:
            QMessageBox.warning(self, "Error", "Invalid selection.")
            return

        # Get member ID from user input
        member_id, ok = QInputDialog.getInt(
            self, 
            "Borrow Book", 
            "Enter Member ID:", 
            value=1, 
            min=1
        )
        
        if not ok:
            return

        book_id = int(book_id_item.text())
        try:
            self.loan_service.borrow_book(member_id, book_id)
            QMessageBox.information(
                self,
                "Borrowed",
                f"Book borrowed successfully. Due in {LoanService.LOAN_DAYS} days.",
            )
            self.View_books()  # Refresh the table
        except ValueError as ve:
            QMessageBox.warning(self, "Cannot Borrow", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while borrowing: {e}")

    def return_selected_book(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a book to return.")
            return

        book_id_item = self.table.item(selected_row, 0)
        if book_id_item is None:
            QMessageBox.warning(self, "Error", "Invalid selection.")
            return

        # Get member ID from user input
        member_id, ok = QInputDialog.getInt(
            self, 
            "Return Book", 
            "Enter Member ID:", 
            value=1, 
            min=1
        )
        
        if not ok:
            return

        book_id = int(book_id_item.text())
        try:
            self.loan_service.return_book_for_member_and_book(member_id, book_id)
            QMessageBox.information(self, "Returned", "Book returned successfully.")
            self.View_books()  # Refresh the table
        except ValueError as ve:
            QMessageBox.warning(self, "Cannot Return", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while returning: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    try:
        print("Starting Library Management System...")
        print(f"Database: {os.getenv('LIB_DB_NAME')}")
        print(f"User: {os.getenv('LIB_DB_USER')}")
        print(f"Host: {os.getenv('LIB_DB_HOST')}")
        print(f"Port: {os.getenv('LIB_DB_PORT')}")
        
        window = LibraryApp()
        print("Window created successfully!")
        window.show()
        window.raise_()  # Bring window to front
        window.activateWindow()  # Activate the window
        print("Window displayed!")
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        error_msg = f"Failed to start application:\n{str(e)}\n\nPlease check the database connection."
        print("=" * 50)
        print("ERROR DETAILS:")
        print("=" * 50)
        print(traceback.format_exc())
        print("=" * 50)
        QMessageBox.critical(None, "Application Error", error_msg)
        sys.exit(1)
