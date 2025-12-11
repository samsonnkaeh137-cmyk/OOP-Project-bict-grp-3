"""
Script to find the correct PostgreSQL port and set up the database.
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def try_connection(user, password, host, port):
    """Try to connect and return True if successful."""
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port,
            connect_timeout=2
        )
        conn.close()
        return True
    except:
        return False

def setup_database(user, password, host, port, target_db):
    """Create database and tables."""
    try:
        # Create database
        conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {target_db}")
            print(f"✓ Created database '{target_db}'")
        else:
            print(f"✓ Database '{target_db}' already exists")
        cur.close()
        conn.close()
        
        # Create tables
        conn = psycopg2.connect(dbname=target_db, user=user, password=password, host=host, port=port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY, username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL, role_id INTEGER NOT NULL REFERENCES roles(id)
            );
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY REFERENCES users(id), full_name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL,
                isbn TEXT NOT NULL, genre TEXT NOT NULL, year TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS loans (
                id SERIAL PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id),
                member_id INTEGER NOT NULL REFERENCES members(id),
                loan_date TIMESTAMPTZ NOT NULL, due_date TIMESTAMPTZ NOT NULL,
                return_date TIMESTAMPTZ
            );
        """)
        print("✓ Created all tables")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    user = "postgres"
    password = "samson"
    host = "localhost"
    target_db = "lirary"
    
    # Try common ports
    ports_to_try = [5432, 5433, 5434]
    
    print("Searching for PostgreSQL server...")
    working_port = None
    
    for port in ports_to_try:
        print(f"Trying port {port}...", end=" ")
        if try_connection(user, password, host, port):
            print("✓ Connected!")
            working_port = port
            break
        else:
            print("✗ Failed")
    
    if not working_port:
        print("\n✗ Could not connect to PostgreSQL on any port.")
        print("\nPlease check:")
        print("  1. PostgreSQL is running")
        print("  2. Username and password are correct")
        print("  3. Check pgAdmin4 for the correct port")
        sys.exit(1)
    
    print(f"\n✓ Found PostgreSQL on port {working_port}")
    print(f"\nSetting up database '{target_db}'...")
    
    if setup_database(user, password, host, working_port, target_db):
        print("\n✓ Setup complete!")
        print(f"\nUse these environment variables:")
        print(f"  $env:LIB_DB_NAME='{target_db}'")
        print(f"  $env:LIB_DB_USER='{user}'")
        print(f"  $env:LIB_DB_PASSWORD='{password}'")
        print(f"  $env:LIB_DB_HOST='{host}'")
        print(f"  $env:LIB_DB_PORT='{working_port}'")
        
        # Save to a file for easy loading
        with open("db_config.txt", "w") as f:
            f.write(f"LIB_DB_NAME={target_db}\n")
            f.write(f"LIB_DB_USER={user}\n")
            f.write(f"LIB_DB_PASSWORD={password}\n")
            f.write(f"LIB_DB_HOST={host}\n")
            f.write(f"LIB_DB_PORT={working_port}\n")
        print("\n✓ Configuration saved to db_config.txt")
    else:
        sys.exit(1)

