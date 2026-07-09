import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Connection Credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "task_manager_db")

def get_db_connection(use_database=True):
    """
    Establishes a connection to the MySQL database.
    If use_database is False, connects to the server without selecting a specific database.
    """
    config = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
    if use_database:
        config["database"] = DB_NAME
    
    return mysql.connector.connect(**config)

def initialize_database():
    """
    Initializes the database by creating the database if it doesn't exist,
    creating the necessary tables (admins and tasks), and seeding initial data.
    """
    try:
        # Step 1: Connect to MySQL server without database to create the database if not exists
        conn = get_db_connection(use_database=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Failed to connect to MySQL server or create database: {err}")
        return False

    try:
        # Step 2: Connect to the created/existing database
        conn = get_db_connection(use_database=True)
        cursor = conn.cursor()

        # Create admins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                admin_id VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )
        ''')

        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(255) NOT NULL,
                employee_name VARCHAR(255) NOT NULL,
                task_title VARCHAR(255) NOT NULL,
                completed VARCHAR(50) NOT NULL DEFAULT 'false'
            )
        ''')

        # Insert default admin if table is empty
        cursor.execute("SELECT * FROM admins WHERE admin_id = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO admins (admin_id, password) VALUES (%s, %s)", ('admin', 'admin123'))
            print("Default admin account created: admin / admin123")

        # Seed sample tasks if the tasks table is empty
        cursor.execute("SELECT COUNT(*) FROM tasks")
        if cursor.fetchone()[0] == 0:
            sample_tasks = [
                ('EMP001', 'John Doe', 'Setup Development Environment', 'false'),
                ('EMP002', 'Jane Smith', 'Design Application Layout', 'true'),
                ('EMP003', 'Bob Johnson', 'Configure Database Schema', 'false')
            ]
            cursor.executemany('''
                INSERT INTO tasks (employee_id, employee_name, task_title, completed) 
                VALUES (%s, %s, %s, %s)
            ''', sample_tasks)
            print("Sample tasks seeded successfully.")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database structure verified and initialized successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"Error during database table initialization: {err}")
        return False

def verify_admin_credentials(admin_id, password):
    """
    Checks if the admin credentials are valid in the database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM admins WHERE admin_id = %s AND password = %s',
            (admin_id, password)
        )
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        return admin
    except mysql.connector.Error as err:
        print(f"Database query error (verify_admin_credentials): {err}")
        return None

def fetch_all_tasks():
    """
    Fetches all tasks from the database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks
    except mysql.connector.Error as err:
        print(f"Database query error (fetch_all_tasks): {err}")
        return []

def update_task_status(task_title, completed_status):
    """
    Updates the completed status of a task by its title.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET completed = %s WHERE task_title = %s',
            (completed_status, task_title)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database query error (update_task_status): {err}")
        return False

if __name__ == '__main__':
    initialize_database()
