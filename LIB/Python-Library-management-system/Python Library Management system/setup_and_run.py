"""
Setup script to create database if needed and populate sample data, then run the app.
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Set environment variables
os.environ['LIB_DB_NAME'] = 'lirary'
os.environ['LIB_DB_USER'] = 'postgres'
os.environ['LIB_DB_PASSWORD'] = 'samson'
os.environ['LIB_DB_HOST'] = 'localhost'
os.environ['LIB_DB_PORT'] = '5432'

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            dbname='postgres',
            user=os.environ['LIB_DB_USER'],
            password=os.environ['LIB_DB_PASSWORD'],
            host=os.environ['LIB_DB_HOST'],
            port=os.environ['LIB_DB_PORT']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (os.environ['LIB_DB_NAME'],))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database '{os.environ['LIB_DB_NAME']}'...")
            cur.execute(f'CREATE DATABASE {os.environ["LIB_DB_NAME"]}')
            print("Database created successfully!")
        else:
            print(f"Database '{os.environ['LIB_DB_NAME']}' already exists.")
        
        cur.close()
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Username and password are correct")
        print("3. PostgreSQL is accessible on localhost:5432")
        sys.exit(1)

if __name__ == "__main__":
    print("Setting up database...")
    create_database_if_not_exists()
    
    print("\nPopulating sample data...")
    from seed_sample_data import main as seed_main
    seed_main()
    
    print("\nStarting Library Management System...")
    from PyQt5.QtWidgets import QApplication
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_window", "main window.py")
    main_window_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_window_module)
    LoginDialog = main_window_module.LoginDialog
    LibraryApp = main_window_module.LibraryApp
    
    app = QApplication(sys.argv)
    from PyQt5.QtWidgets import QDialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        if login_dialog.user_id is None or login_dialog.role_name is None:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Error", "Login failed: missing user information.")
            sys.exit(1)
        
        window = LibraryApp(
            user_id=login_dialog.user_id,
            role_name=login_dialog.role_name,
        )
        window.show()
        sys.exit(app.exec_())

