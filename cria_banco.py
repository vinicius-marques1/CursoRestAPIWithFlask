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
