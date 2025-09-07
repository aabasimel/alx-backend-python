0. Getting Started with Python Generators
Overview

This project introduces Python generators in the context of working with an SQL database. The main goal is to create a generator that streams rows from a MySQL database one by one, allowing efficient processing of large datasets.

Files

seed.py – Contains functions to:

Connect to MySQL server and the ALX_prodev database.

Create the database and user_data table if they do not exist.

Insert sample data from user_data.csv.

0-main.py – Script to test the functions in seed.py.

Database Setup

The project uses a MySQL database named ALX_prodev with a table user_data having the following structure:

Column	Type	Constraints
user_id	UUID	Primary Key, Indexed
name	VARCHAR	NOT NULL
email	VARCHAR	NOT NULL
age	DECIMAL	NOT NULL

Sample data is loaded from user_data.csv.

Functions in seed.py

connect_db()
Connects to the MySQL database server.

create_database(connection)
Creates the ALX_prodev database if it does not exist.

connect_to_prodev()
Connects to the ALX_prodev database.

create_table(connection)
Creates the user_data table if it does not exist with the required fields.

insert_data(connection, data)
Inserts data into the database if it does not already exist.

Usage

Run the main script to initialize the database, create the table, insert data, and fetch sample rows:

python 0-main.py


Expected output:

connection successful
Table user_data created successfully
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67),
 ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119),
 ...]

Requirements

Python 3.x

MySQL server

mysql-connector-python library:

pip install mysql-connector-python
