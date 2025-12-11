# Set PostgreSQL environment variables
$env:LIB_DB_NAME = "lirary"
$env:LIB_DB_USER = "postgres"
$env:LIB_DB_PASSWORD = "samson"
$env:LIB_DB_HOST = "localhost"
$env:LIB_DB_PORT = "5432"

# Install required packages if not already installed
Write-Host "Installing required packages..."
py -m pip install psycopg2-binary PyQt5 --quiet

# Run seed script to populate sample data
Write-Host "Populating database with sample data..."
py seed_sample_data.py

# Run the main application
Write-Host "Starting Library Management System..."
py "main window.py"

