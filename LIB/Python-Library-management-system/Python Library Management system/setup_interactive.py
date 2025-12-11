"""
Interactive script to set up the database with user-provided credentials.
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def test_connection(user, password, host, port, dbname='postgres'):
    """Test PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False

def create_database_and_tables(user, password, host, port, target_db):
    """Create database and all tables."""
    try:
        # Connect to postgres database
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Create database if not exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {target_db}")
            print(f"✓ Created database '{target_db}'")
        else:
            print(f"✓ Database '{target_db}' already exists")
        
        cur.close()
        conn.close()
        
        # Connect to target database and create tables
        conn = psycopg2.connect(
            dbname=target_db,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        tables = [
            ("roles", """
                CREATE TABLE IF NOT EXISTS roles (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                );
            """),
            ("users", """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role_id INTEGER NOT NULL REFERENCES roles(id)
                );
            """),
            ("members", """
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY REFERENCES users(id),
                    full_name TEXT NOT NULL
                );
            """),
            ("books", """
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    year TEXT NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 1
                );
            """),
            ("loans", """
                CREATE TABLE IF NOT EXISTS loans (
                    id SERIAL PRIMARY KEY,
                    book_id INTEGER NOT NULL REFERENCES books(id),
                    member_id INTEGER NOT NULL REFERENCES members(id),
                    loan_date TIMESTAMPTZ NOT NULL,
                    due_date TIMESTAMPTZ NOT NULL,
                    return_date TIMESTAMPTZ
                );
            """)
        ]
        
        for table_name, sql in tables:
            cur.execute(sql)
            print(f"✓ Created/verified table '{table_name}'")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PostgreSQL Database Setup")
    print("=" * 60)
    print("\nPlease provide your PostgreSQL credentials:")
    print("(Press Enter to use defaults)")
    
    user = input("\nUsername [postgres]: ").strip() or "postgres"
    password = input("Password [samson]: ").strip() or "samson"
    host = input("Host [localhost]: ").strip() or "localhost"
    port_input = input("Port [5432]: ").strip() or "5432"
    
    try:
        port = int(port_input)
    except ValueError:
        print("Invalid port number, using 5432")
        port = 5432
    
    target_db = input("Database name [lirary]: ").strip() or "lirary"
    
    print(f"\nTesting connection to PostgreSQL server...")
    if not test_connection(user, password, host, port):
        print(f"\n✗ Connection failed!")
        print("\nPlease check:")
        print("  1. PostgreSQL service is running")
        print("  2. Credentials are correct")
        print("  3. Port number is correct")
        print("\nCommon PostgreSQL ports:")
        print("  - PostgreSQL 14: Usually 5432")
        print("  - PostgreSQL 17: Usually 5433 (if both are installed)")
        sys.exit(1)
    
    print("✓ Connection successful!")
    print(f"\nCreating database '{target_db}' and tables...")
    
    if create_database_and_tables(user, password, host, port, target_db):
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print(f"\nDatabase: {target_db}")
        print(f"User: {user}")
        print(f"Host: {host}:{port}")
        print("\nNext steps:")
        print("  1. Set environment variables:")
        print(f"     $env:LIB_DB_NAME='{target_db}'")
        print(f"     $env:LIB_DB_USER='{user}'")
        print(f"     $env:LIB_DB_PASSWORD='{password}'")
        print(f"     $env:LIB_DB_HOST='{host}'")
        print(f"     $env:LIB_DB_PORT='{port}'")
        print("  2. Run: py seed_sample_data.py")
        print("  3. Run: py \"main window.py\"")
    else:
        print("\n✗ Setup failed!")
        sys.exit(1)

