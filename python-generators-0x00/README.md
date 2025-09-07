# 0. Getting Started with Python Generators

## Overview

This project introduces **Python generators** in the context of working with an SQL database. The main goal is to create a generator that streams rows from a MySQL database one by one, allowing efficient processing of large datasets.

---

## Files

- `seed.py` – Contains functions to:
  - Connect to MySQL server and the `ALX_prodev` database.
  - Create the database and `user_data` table if they do not exist.
  - Insert sample data from `user_data.csv`.
- `0-main.py` – Script to test the functions in `seed.py`.

---

## Database Setup

The project uses a MySQL database named **ALX_prodev** with a table **user_data** having the following structure:

| Column   | Type      | Constraints                       |
|----------|-----------|----------------------------------|
| user_id  | UUID      | Primary Key, Indexed             |
| name     | VARCHAR   | NOT NULL                         |
| email    | VARCHAR   | NOT NULL                         |
| age      | DECIMAL   | NOT NULL                         |

Sample data is loaded from `user_data.csv`.

---

## Functions in `seed.py`

1. `connect_db()`  
   Connects to the MySQL database server.

2. `create_database(connection)`  
   Creates the `ALX_prodev` database if it does not exist.

3. `connect_to_prodev()`  
   Connects to the `ALX_prodev` database.

4. `create_table(connection)`  
   Creates the `user_data` table if it does not exist with the required fields.

5. `insert_data(connection, data)`  
   Inserts data into the database if it does not already exist.

---

## Usage

Run the main script to initialize the database, create the table, insert data, and fetch sample rows:

```bash
python 0-main.py
