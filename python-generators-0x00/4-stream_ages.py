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

def stream_user_ages():
        """Generator that yields user ages one by one from user_data table"""
        try:
                connection=mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="bw123bw",
                        database="ALX_prodev"

                )
                cursor=connection.cursor(dictionary=True)
                cursor.execute("SELECT age FROM user_data")

                for row in cursor:
                        yield row['age']
        except Exception as e:
                print(f"Error:{e}")
        finally:
                if cursor:
                        cursor.close()
                if connection and connection.is_connected():
                        connection.close()

def average_age():
        total=0
        count=0
        for agae in stream_user_ages():
                total+=agae
                count+=1
        if count==0:
                return 0
        return total/count

if __name__ == "__main__":
        avg=average_age()
        print(f"Average age of users: {avg}")
                

