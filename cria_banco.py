import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, " \
"name text, stars real, daily real, city text)"

criar_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Alpha Hotel', 4.3, 420.34, 'Rio de Janeiro')"

cursor.execute(cria_tabela)
cursor.execute(criar_hotel)

connection.commit()
connection.close()


# This code is a simple SQLite database creation script. 
# It connects to a SQLite database file named 'banco.db', 
# creates a table named 'hoteis' if it doesn't already exist, 
# and inserts a record into that table. The table has columns 
# for hotel ID, name, star rating, daily rate, and city. 
# After executing the SQL commands, it commits the changes and closes the connection to the database.

# But in the project we use the flask_sqlalchemy python package.
# This package is a Flask extension that adds support for SQLAlchemy,
# which is a SQL toolkit and Object-Relational Mapping (ORM) system for Python.
# It allows you to interact with databases in a more Pythonic way,
# using classes and objects instead of writing raw SQL queries.
# The SQLAlchemy package provides a high-level API for database operations,
# making it easier to work with databases in Flask applications.