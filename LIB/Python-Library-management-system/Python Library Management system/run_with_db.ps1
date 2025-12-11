# Script to run Library Management System with database setup
# You can modify the credentials below if needed

param(
    [string]$DBUser = "postgres",
    [string]$DBPassword = "samson",
    [string]$DBName = "library",
    [string]$DatabaseHost = "localhost",
    [string]$DBPort = "5433"
)

Write-Host "========================================"
Write-Host "Library Management System"
Write-Host "========================================"
Write-Host "Database: $DBName"
Write-Host "User: $DBUser"
Write-Host "Host: ${DatabaseHost}:${DBPort}"
Write-Host ""

# Set environment variables
$env:LIB_DB_NAME = $DBName
$env:LIB_DB_USER = $DBUser
$env:LIB_DB_PASSWORD = $DBPassword
$env:LIB_DB_HOST = $DatabaseHost
$env:LIB_DB_PORT = $DBPort

# Find Python
$pythonCmd = "py"
if (-not (Get-Command $pythonCmd -ErrorAction SilentlyContinue)) {
    $pythonCmd = "python"
}

# Install packages
Write-Host "Checking packages..."
& $pythonCmd -m pip install --quiet --upgrade psycopg2-binary PyQt5 2>$null

# Try to populate sample data
Write-Host "Populating sample data..."
& $pythonCmd seed_sample_data.py 2>&1 | Out-String | Write-Host

# Run the application
Write-Host "Starting application..."
Write-Host ""
& $pythonCmd "main window.py"

