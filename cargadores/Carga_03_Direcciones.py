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


def carga_direcciones(archivo_csv, tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        Direcciones = csv.reader(f, delimiter=';')
        next(Direcciones)  # me salto la primera fila (cabecera)
        malas = []
        for direccion in Direcciones:
            cursor.execute(
                '''SELECT id FROM Clientes
                WHERE Clientes.email = %s''',
                (direccion[1],)
            )
            cliente = cursor.fetchone()
            if cliente:            
                try:
                    SQL = f"INSERT INTO {tabla} (direccion, cut_comuna) VALUES (%s, %s)"
                    data = (direccion[4], direccion[5],)
                    cursor.execute(SQL, data)
                except Exception as error:
                    if not isinstance(error, psycopg2.IntegrityError) and error.pgcode == '23505':
                        print(f"Error de integridad: {error}")
                        malas += direccion
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Tupla Cargada:", data)
    print("tuplas para arreglar:",malas)

# Conexión a la base de datos
with psycopg2.connect(
    host= DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_USER_PASSWORD,
    port=DATABASE_PORT,
    database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = ('IIC2413-Entrega-2/data/clientes.csv')
            nombre_tabla = 'direcciones'
            carga_direcciones(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")

