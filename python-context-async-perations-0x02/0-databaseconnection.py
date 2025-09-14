#!/usr/bin/env python3

"""
0-databaseconnection.py
Custom class-based context manager for Database connections
"""

import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        # Get database credentials from environment variables or defaults
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "root")
        self.database = os.getenv("DB_NAME", "users.db")
        self.connection = None

    def __enter__(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """close the database connection"""
        if self.connection:
            self.connection.close()
        return False

