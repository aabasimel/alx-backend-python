###!/usr/bin/env python3

"""
1-execute.py
Custom context manager to execute a query with parameters
"""

import pymysql
from dotenv import load_dotenv
import os

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "test_db")
        self.query = query
        self.params = params
        self.connection = None
        self.result = None

    def __enter__(self):
        """Open the connection, execute the query, and return the result."""

        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor

        )

        with self.connection.cursor() as cursor:
            cursor.execute(self.query, self.params)
            self.result = cursor.fetchall()
        return False
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """close the database connection"""
        if self.connection:
            self.connection.close()
        return False
    

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)

    with ExecuteQuery(query, params) as result:
        for row in result:
            print(row)

        