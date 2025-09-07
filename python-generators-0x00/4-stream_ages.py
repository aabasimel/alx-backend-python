#!/usr/bin/python3

# Memory-Efficient Aggregation with Generators
# mandatory
# Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

# Instruction:

# Implement a generator stream_user_ages() that yields user ages one by one.

# Use the generator in a different function to calculate the average age without loading the entire dataset into memory

# Your script should print Average age of users: average age

# You must use no more than two loops in your script

# You are not allowed to use the SQL AVERAGE

import mysql.connector
from seed import connect_to_prodev  
def stream_user_ages():
    """Generator that yields user ages one by one"""
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row['age']
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def calculate_average_age():
    """Calculates average age without loading entire dataset into memory"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count > 0:
        average = total / count
        print(f"Average age of users: {average}")
    else:
        print("No users found.")

if __name__ == "__main__":
    calculate_average_age()
