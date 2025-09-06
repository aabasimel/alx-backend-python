import pymysql
import csv
import uuid

DB_NAME = "ALX_prodev"

def connect_db():
    """Connect to the MySQL server (without specifying DB)."""
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",   
            password="Sh123&*abc",  
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor,
            autocommit=True
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"Database {DB_NAME} created or already exists")
    except Exception as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",   
            password="Sh123&*abc",
            database=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor,
            autocommit=True
        )
        return connection
    except Exception as e:
        print(f"Error connecting to {DB_NAME}: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id CHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL NOT NULL,
                    INDEX (user_id)
                )
            """)
            print("Table user_data created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from a CSV file into user_data if not already present."""
    try:
        with open(csv_file, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            with connection.cursor() as cursor:
                for row in reader:
                    user_id = str(uuid.uuid4())
                    name = row["name"]
                    email = row["email"]
                    age = row["age"]

                    # Avoid inserting duplicates (based on email)
                    cursor.execute("SELECT user_id FROM user_data WHERE email=%s", (email,))
                    if cursor.fetchone():
                        continue

                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
            print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")

