"""Test PostgreSQL connection with provided credentials."""
import os
import psycopg2

# Set credentials
dbname = 'library'
user = 'postgres'
password = 'samson'
host = 'localhost'
port = 5433

print("Testing PostgreSQL connection...")
print(f"Database: {dbname}")
print(f"User: {user}")
print(f"Host: {host}")
print(f"Port: {port}")
print()

# Try connecting to postgres database first (to create library if needed)
try:
    print("Connecting to PostgreSQL server...")
    conn = psycopg2.connect(
        dbname='postgres',
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("✓ Successfully connected to PostgreSQL server!")
    
    # Check if database exists
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
    exists = cur.fetchone()
    
    if not exists:
        print(f"\nDatabase '{dbname}' does not exist. Creating it...")
        cur.execute(f'CREATE DATABASE {dbname}')
        print(f"✓ Database '{dbname}' created successfully!")
    else:
        print(f"\n✓ Database '{dbname}' already exists.")
    
    cur.close()
    conn.close()
    
    # Now try connecting to the actual database
    print(f"\nConnecting to database '{dbname}'...")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print(f"✓ Successfully connected to database '{dbname}'!")
    conn.close()
    
    print("\n✓ All connection tests passed!")
    print("You can now run the application.")
    
except psycopg2.OperationalError as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nPossible issues:")
    print("  1. PostgreSQL service is not running")
    print("  2. Wrong username or password")
    print("  3. PostgreSQL is not accessible on localhost:5432")
    print("  4. Firewall blocking the connection")
    print("\nTo check if PostgreSQL is running:")
    print("  - Windows: Open Services and check 'postgresql-x64-XX' service")
    print("  - Or run: Get-Service | Where-Object {$_.Name -like '*postgres*'}")

