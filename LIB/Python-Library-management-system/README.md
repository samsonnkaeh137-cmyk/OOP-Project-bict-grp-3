# Python-Library-management-system

This is a **Python-based Library Management System** that helps users manage books efficiently. Built with **PyQt Designer** for the graphical interface and **SQLite3** for database storage, this system allows users to **add, update, delete, and search** book records seamlessly.

## Features

- 📖 Add new books with details (Title, Author, ISBN, Genre, etc.)
- 🔍 Search for books by title, author, or ISBN
- ✏️ Update book records easily
- 🗑️ Delete books from the database
- 🖥️ User-friendly graphical interface with PyQt
- 🗂️ SQLite-backed persistence (ships with a sample `library.db`)

## 🛠️ Technologies Used

- **Python 3** – Core programming language
- **PyQt5** – GUI framework (interface designed in Qt Designer)
- **SQLite3** – Lightweight database for storing book records (built into Python)
- **Standard library** modules only beyond PyQt5

## 📂 Project Structure

- `Python Library Management system/main window.py` — PyQt5 entry point
- `Python Library Management system/Database.py` — database helper layer
- `Python Library Management system/infrastructure/db.py` — SQLite connection utilities
- `Python Library Management system/domain`, `services`, `repositories` — domain, service, and repository logic
- `Library.ui` — Qt Designer UI file
- `library.db` / `Database.db` — sample SQLite databases
- `seed_sample_data.py` — optional script to seed demo data

## 🛠️ Prerequisites

- Python 3.8+ installed and on PATH (`python3 --version`)
- Pip available (`python3 -m pip --version`)
- Internet access to install PyQt5 from PyPI (or a local wheel if offline)

## 🚀 Installation & Setup

Follow these steps to run the project on your machine.

1. Clone the repository

```bash
git clone https://github.com/JosephineGegra/Python-Library-management-system.git
cd Python-Library-management-system
```

2. (Recommended) create & activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

3. Install dependencies (PyQt5 is the only external package)

```bash
python3 -m pip install --upgrade pip
python3 -m pip install PyQt5
```

4. (Optional) seed demo data into the SQLite DB

```bash
cd "Python Library Management system"
python3 seed_sample_data.py
cd ..
```

## ▶️ Run the application

From the repository root:

```bash
cd "Python Library Management system"
python3 "main window.py"
```

The UI should launch and connect to the bundled `library.db`. If you want a fresh database, delete or rename `library.db` before running and the app will create a new one.

## 🧩 Troubleshooting

- **PyQt5 not found**: ensure step 3 finished successfully and you’re inside the virtualenv (`which python` / `where python`).
- **Pip cannot download packages**: your environment may block network; install PyQt5 from a local wheel or allow network for `pip`.
- **DB permission/locked errors**: close other apps using the DB file and retry; you can also remove `library.db` to start clean.

## 🗄️ PostgreSQL schema (for server deployments)

The app can use PostgreSQL via `Database.py`. Set environment variables `LIB_DB_NAME`, `LIB_DB_USER`, `LIB_DB_PASSWORD`, and optionally `LIB_DB_HOST`/`LIB_DB_PORT`. Run this SQL to create the table:

```sql
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL,
    genre TEXT NOT NULL,
    year TEXT NOT NULL
);
```
