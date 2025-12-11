# Library Management System - Setup and Run Script
# Make sure PostgreSQL is running and credentials are correct

Write-Host "========================================"
Write-Host "Library Management System Setup"
Write-Host "========================================"

# Set PostgreSQL environment variables
$env:LIB_DB_NAME = "lirary"
$env:LIB_DB_USER = "postgres"
$env:LIB_DB_PASSWORD = "samson"
$env:LIB_DB_HOST = "localhost"
$env:LIB_DB_PORT = "5432"

Write-Host "Environment variables set:"
Write-Host "  Database: $env:LIB_DB_NAME"
Write-Host "  User: $env:LIB_DB_USER"
Write-Host "  Host: $env:LIB_DB_HOST"
Write-Host "  Port: $env:LIB_DB_PORT"
Write-Host ""

# Change to the application directory
Set-Location "Python Library Management system"

# Check if Python is available
$pythonCmd = "py"
if (-not (Get-Command $pythonCmd -ErrorAction SilentlyContinue)) {
    $pythonCmd = "python"
    if (-not (Get-Command $pythonCmd -ErrorAction SilentlyContinue)) {
        Write-Host "ERROR: Python not found. Please install Python."
        exit 1
    }
}

# Install required packages
Write-Host "Installing required packages (PyQt5 and psycopg2-binary)..."
& $pythonCmd -m pip install --quiet psycopg2-binary PyQt5
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install packages"
    exit 1
}
Write-Host "Packages installed successfully!"
Write-Host ""

# Try to create database and populate sample data
Write-Host "Setting up database and populating sample data..."
& $pythonCmd setup_and_run.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Database setup failed."
    Write-Host "Please check:"
    Write-Host "  1. PostgreSQL is running"
    Write-Host "  2. Username: $env:LIB_DB_USER"
    Write-Host "  3. Password: $env:LIB_DB_PASSWORD"
    Write-Host "  4. Database '$env:LIB_DB_NAME' exists or can be created"
    Write-Host ""
    Write-Host "You can also run the application directly with:"
    Write-Host "  py `"main window.py`""
    exit 1
}

