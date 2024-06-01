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
    malas = []
    with open(archivo_csv, 'r') as f:
        Platos = csv.reader(f, delimiter=';')
        next(Platos)  # Saltar la primera fila (cabecera)
        for plato in Platos:
            cursor.execute(
                "SELECT id FROM platos WHERE nombre = %s",
                (plato[1],)
            )
            id_plato = cursor.fetchone()
            cursor.execute(
                "SELECT id FROM Restaurantes WHERE nombre = %s",
                (plato[10],)
            )
            id_restaurante = cursor.fetchone()

            if id_plato and id_restaurante:
                try:

                    SQL = f"INSERT INTO {tabla} (id ,id_plato, id_restaurante, disponibilidad, porciones, precio, tiempo_prep) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    data = (plato[0],id_plato[0], id_restaurante[0], plato[3], plato[7], plato[8], plato[9],)
                    cursor.execute(SQL, data)
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback en caso de error
                    malas.append((error,data, plato[1],plato[10]))
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Datos Guardados:", data)
    print("-----MALAS-----")
    for mala in malas:
        print(mala)

# Conexión a la base de datos
with psycopg2.connect(
    host= DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_USER_PASSWORD,
    port=DATABASE_PORT,
    database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = ('IIC2413-Entrega-2/data/platos.csv')
            nombre_tabla = 'platos_restaurantes'
            carga_plato_restaurante(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")
