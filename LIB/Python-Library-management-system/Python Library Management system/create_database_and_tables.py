"""
Script to create the database and all required tables.
Run this first before running the application.
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration
DB_CONFIG = {
    'dbname': 'postgres',  # Connect to default postgres database first
    'user': 'postgres',
    'password': 'samson',
    'host': 'localhost',
    'port': 5433
}

TARGET_DB = 'library'

def create_database():
    """Create the database if it doesn't exist."""
    try:
        print(f"Connecting to PostgreSQL server as user '{DB_CONFIG['user']}'...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TARGET_DB,))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database '{TARGET_DB}'...")
            cur.execute(f"CREATE DATABASE {TARGET_DB}")
            print(f"✓ Database '{TARGET_DB}' created successfully!")
        else:
            print(f"✓ Database '{TARGET_DB}' already exists.")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Connection failed: {e}")
        print("\nPlease verify:")
        print(f"  1. PostgreSQL is running")
        print(f"  2. Username: {DB_CONFIG['user']}")
        print(f"  3. Password: {DB_CONFIG['password']}")
        print(f"  4. Port: {DB_CONFIG['port']}")
        return False

def create_tables():
    """Create all required tables in the database."""
    try:
        print(f"\nConnecting to database '{TARGET_DB}'...")
        conn = psycopg2.connect(
            dbname=TARGET_DB,
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("Creating tables...")
        
        # Create roles table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );
        """)
        print("✓ Created 'roles' table")
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role_id INTEGER NOT NULL REFERENCES roles(id)
            );
        """)
        print("✓ Created 'users' table")
        
        # Create members table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY REFERENCES users(id),
                full_name TEXT NOT NULL
            );
        """)
        print("✓ Created 'members' table")
        
        # Create books table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL,
                genre TEXT NOT NULL,
                year TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1
            );
        """)
        print("✓ Created 'books' table")
        
        # Create loans table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL REFERENCES books(id),
                member_id INTEGER NOT NULL REFERENCES members(id),
                loan_date TIMESTAMPTZ NOT NULL,
                due_date TIMESTAMPTZ NOT NULL,
                return_date TIMESTAMPTZ
            );
        """)
        print("✓ Created 'loans' table")
        
        cur.close()
        conn.close()
        print("\n✓ All tables created successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"\n✗ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Database Setup Script")
    print("=" * 50)
    
    if not create_database():
        sys.exit(1)
    
    if not create_tables():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nYou can now run the application with:")
    print("  py seed_sample_data.py  # Populate sample data")
    print("  py \"main window.py\"     # Run the application")

