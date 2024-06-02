import csv
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_USER_PASSWORD = os.getenv('DATABASE_USER_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')

def carga_restaurantes(archivo_csv, tabla,cursor, conn):
    with open(archivo_csv, mode='r', encoding='mac_roman') as f:
        Restaurantes = csv.reader(f, delimiter=';')
        next(Restaurantes)  # me salto la primera fila (cabecera)
        tuplas_malas = []
        for restaurant in Restaurantes:
            try:
                SQL = f"INSERT INTO {tabla} (nombre, vigencia, estilo, repartoming) VALUES (%s, %s, %s, %s)"
                data = (restaurant[0], restaurant[1], restaurant[2], restaurant[3],)
                cursor.execute(SQL, data)
            except Exception as error:
                if not isinstance(error, psycopg2.IntegrityError):
                    print(f"Error de integridad: {error}")
                    tuplas_malas += restaurant
                conn.rollback()  # Rollback para evitar transacciones inconsistentes
            else:
                conn.commit()  # Commit para guardar los cambios
                print("Tupla guardada:", restaurant)
    print("MALAS: ",tuplas_malas)

# Conexión a la base de datos
with psycopg2.connect(
    host= DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_USER_PASSWORD,
    port=DATABASE_PORT,
    database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = os.path.join('..','data','restaurantes2.csv')
            nombre_tabla = 'restaurantes'
            carga_restaurantes(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")
