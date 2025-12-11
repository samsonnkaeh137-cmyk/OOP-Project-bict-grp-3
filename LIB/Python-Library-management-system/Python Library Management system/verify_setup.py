"""Verify database setup and tables."""
import os
os.environ['LIB_DB_NAME'] = 'library'
os.environ['LIB_DB_USER'] = 'postgres'
os.environ['LIB_DB_PASSWORD'] = 'samson'
os.environ['LIB_DB_HOST'] = 'localhost'
os.environ['LIB_DB_PORT'] = '5433'

from infrastructure.db import connection_scope

try:
    with connection_scope() as conn:
        cur = conn.cursor()
        
        # Check tables
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename")
        tables = [row[0] for row in cur.fetchall()]
        print(f"✓ Found {len(tables)} tables: {', '.join(tables)}")
        
        # Check books
        cur.execute("SELECT COUNT(*) FROM books")
        book_count = cur.fetchone()[0]
        print(f"✓ Books in database: {book_count}")
        
        # Check users
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        print(f"✓ Users in database: {user_count}")
        
        print("\n✓ Database setup verified successfully!")
        print("\nThe application should be running. Check your taskbar for the GUI window.")
        
except Exception as e:
    print(f"✗ Error: {e}")

