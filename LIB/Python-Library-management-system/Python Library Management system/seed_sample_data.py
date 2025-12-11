"""
Simple script to insert sample book data into the PostgreSQL `books` table
using the clean architecture BookService.

Run from the project folder:

    python3 seed_sample_data.py
"""

import os
from services.book_service import BookService
from infrastructure.db import connection_scope


def clear_existing_books():
    """Clear all existing books from the database."""
    try:
        with connection_scope() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM books")
                print("✓ Cleared existing books from database.")
    except Exception as e:
        print(f"Note: Could not clear existing books: {e}")


def main():
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
        os.environ['LIB_DB_PORT'] = '5433'
    
    service = BookService()
    
    # Clear existing books first
    clear_existing_books()

    sample_books = [
        # Fiction & Literature
        ("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Fiction", "1960"),
        ("1984", "George Orwell", "9780451524935", "Dystopian Fiction", "1949"),
        ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Classic Literature", "1925"),
        ("Pride and Prejudice", "Jane Austen", "9780141439518", "Romance", "1813"),
        ("The Catcher in the Rye", "J.D. Salinger", "9780316769488", "Fiction", "1951"),
        
        # Science & Technology
        ("A Brief History of Time", "Stephen Hawking", "9780553380163", "Science", "1988"),
        ("Sapiens", "Yuval Noah Harari", "9780062316097", "History", "2011"),
        ("The Selfish Gene", "Richard Dawkins", "9780192860927", "Biology", "1976"),
        ("Cosmos", "Carl Sagan", "9780345331359", "Astronomy", "1980"),
        
        # Business & Self-Help
        ("The 7 Habits of Highly Effective People", "Stephen R. Covey", "9780743269513", "Self-Help", "1989"),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "9780374533557", "Psychology", "2011"),
        ("Atomic Habits", "James Clear", "9780735211292", "Self-Help", "2018"),
        
        # Mystery & Thriller
        ("The Girl with the Dragon Tattoo", "Stieg Larsson", "9780307269751", "Mystery", "2005"),
        ("Gone Girl", "Gillian Flynn", "9780307588364", "Thriller", "2012"),
        ("The Da Vinci Code", "Dan Brown", "9780307277671", "Mystery", "2003"),
        
        # Fantasy & Science Fiction
        ("The Lord of the Rings", "J.R.R. Tolkien", "9780544003415", "Fantasy", "1954"),
        ("Dune", "Frank Herbert", "9780441013593", "Science Fiction", "1965"),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "9780747532699", "Fantasy", "1997"),
        
        # Programming & Computer Science
        ("Clean Code", "Robert C. Martin", "9780132350884", "Software Engineering", "2008"),
        ("The Pragmatic Programmer", "Andrew Hunt", "9780201616224", "Software Engineering", "1999"),
        ("Introduction to Algorithms", "Cormen et al.", "9780262033848", "Computer Science", "2009"),
        ("Python Crash Course", "Eric Matthes", "9781593276034", "Programming", "2015"),
    ]

    for title, author, isbn, genre, year in sample_books:
        service.add_book(title, author, isbn, genre, year)

    print(f"Inserted {len(sample_books)} sample books into the database.")


if __name__ == "__main__":
    main()


