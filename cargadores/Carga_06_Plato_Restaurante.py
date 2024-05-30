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

def carga_plato_restaurante(archivo_csv, tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        Platos = csv.reader(f)
        next(Platos)  # Saltar la primera fila (cabecera)
        for plato in Platos:
            cursor.execute(
                "SELECT Platos.id, Restaurantes.id FROM Restaurantes, Platos WHERE Platos.nombre = %s AND Restaurantes.nombre = %s",
                (plato[1], plato[10])
            )
            resultado = cursor.fetchone()

            if resultado:
                try:
                    SQL = f"INSERT INTO {tabla} (id_plato, id_restaurante) VALUES (%s, %s)"
                    data = (resultado[0], resultado[1],)
                    cursor.execute(SQL, data)
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback en caso de error
                else:
                    conn.commit()  # Commit para guardar los cambios

# Conexión a la base de datos
with psycopg2.connect(
    host= DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_USER_PASSWORD,
    port=DATABASE_PORT,
    database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = ('IIC2413-Entrega-2/data/restaurantes.csv')
            nombre_tabla = 'restaurantes'
            carga_plato_restaurante(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")
