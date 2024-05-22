import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(dbname ='entrega_2',user = 'manuel',host = '127.0.0.1',password = 'worm33')
    cursor = connection.cursor()
    print(connection.get_dsn_parameters(), "\n")
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Estas conectado a: ", record)
except (Exception, Error) as error:
    print("I am unable to connect to the database")
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
