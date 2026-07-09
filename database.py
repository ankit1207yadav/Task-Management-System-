import os
import sqlite3
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Connection Credentials for MySQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "task_manager_db")

# Flag to dynamically handle SQLite fallback if MySQL is unavailable
_use_sqlite = os.getenv("USE_SQLITE", "False").lower() == "true"

def get_db_connection(use_database=True):
    """
    Establishes a connection to either MySQL or SQLite.
    If MySQL connection fails, it automatically switches to SQLite fallback.
    """
    global _use_sqlite
    
    if _use_sqlite:
        conn = sqlite3.connect("local_database.db")
        conn.row_factory = sqlite3.Row
        return conn

    try:
        config = {
            "host": DB_HOST,
            "port": DB_PORT,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "connect_timeout": 3  # Fast fail-over if server is stopped
        }
        if use_database:
            config["database"] = DB_NAME
        
        return mysql.connector.connect(**config)
    except Exception as err:
        print(f"\n[Warning] MySQL Connection failed: {err}")
        print("[System] Automatically switching to local SQLite database fallback (local_database.db)...\n")
        _use_sqlite = True
        
        conn = sqlite3.connect("local_database.db")
        conn.row_factory = sqlite3.Row
        return conn

def get_cursor(conn):
    """
    Helper to get the appropriate dictionary-formatted cursor based on active driver.
    """
    if _use_sqlite:
        return conn.cursor()
    return conn.cursor(dictionary=True)

def get_placeholder():
    """
    Returns SQL placeholder depending on active database driver.
    """
    return "?" if _use_sqlite else "%s"

def initialize_database():
    """
    Initializes the database by creating tables and seeding initial data.
    """
    global _use_sqlite
    
    # Try connecting. If MySQL fails, get_db_connection sets _use_sqlite = True
    try:
        if not _use_sqlite:
            # MySQL only: Create database if it doesn't exist
            conn = get_db_connection(use_database=False)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
            cursor.close()
            conn.close()
    except Exception as err:
        print(f"[Warning] Failed to initialize MySQL schema: {err}")
        print("[System] Falling back to SQLite database.")
        _use_sqlite = True

    try:
        conn = get_db_connection(use_database=True)
        cursor = conn.cursor()

        # Create admins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                admin_id VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )
        ''')

        # Create tasks table (adjust auto-increment syntax for SQLite vs MySQL)
        if _use_sqlite:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id VARCHAR(255) NOT NULL,
                    employee_name VARCHAR(255) NOT NULL,
                    task_title VARCHAR(255) NOT NULL,
                    completed VARCHAR(50) NOT NULL DEFAULT 'false'
                )
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INT AUTO_INCREMENT PRIMARY KEY,
                    employee_id VARCHAR(255) NOT NULL,
                    employee_name VARCHAR(255) NOT NULL,
                    task_title VARCHAR(255) NOT NULL,
                    completed VARCHAR(50) NOT NULL DEFAULT 'false'
                )
            ''')

        # Check and insert default admin
        placeholder = get_placeholder()
        cursor.execute(f"SELECT * FROM admins WHERE admin_id = {placeholder}", ('admin',))
        if not cursor.fetchone():
            cursor.execute(f"INSERT INTO admins (admin_id, password) VALUES ({placeholder}, {placeholder})", ('admin', 'admin123'))
            print("Default admin account created: admin / admin123")

        # Seed sample tasks
        cursor.execute("SELECT COUNT(*) FROM tasks")
        row = cursor.fetchone()
        count = row[0] if isinstance(row, tuple) else row['COUNT(*)'] if isinstance(row, dict) else row[0]
        if count == 0:
            sample_tasks = [
                ('EMP001', 'John Doe', 'Setup Development Environment', 'false'),
                ('EMP002', 'Jane Smith', 'Design Application Layout', 'true'),
                ('EMP003', 'Bob Johnson', 'Configure Database Schema', 'false')
            ]
            cursor.executemany(f'''
                INSERT INTO tasks (employee_id, employee_name, task_title, completed) 
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
            ''', sample_tasks)
            print("Sample tasks seeded successfully.")

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database ({'SQLite' if _use_sqlite else 'MySQL'}) initialized successfully.")
        return True
    except Exception as err:
        print(f"Error during database table initialization: {err}")
        return False

def verify_admin_credentials(admin_id, password):
    """
    Checks if the admin credentials are valid.
    """
    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        placeholder = get_placeholder()
        cursor.execute(
            f'SELECT * FROM admins WHERE admin_id = {placeholder} AND password = {placeholder}',
            (admin_id, password)
        )
        row = cursor.fetchone()
        admin = dict(row) if (_use_sqlite and row) else row
        cursor.close()
        conn.close()
        return admin
    except Exception as err:
        print(f"Database query error (verify_admin_credentials): {err}")
        return None

def fetch_all_tasks():
    """
    Fetches all tasks.
    """
    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        tasks = [dict(r) for r in rows] if _use_sqlite else rows
        cursor.close()
        conn.close()
        return tasks
    except Exception as err:
        print(f"Database query error (fetch_all_tasks): {err}")
        return []

def update_task_status(task_title, completed_status):
    """
    Updates the completed status of a task by its title.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()
        cursor.execute(
            f'UPDATE tasks SET completed = {placeholder} WHERE task_title = {placeholder}',
            (completed_status, task_title)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"Database query error (update_task_status): {err}")
        return False

if __name__ == '__main__':
    initialize_database()
