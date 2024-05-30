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

def carga_comuna(archivo_csv, tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        comunas = csv.reader(f)
        next(comunas)  # me salto la primera fila (cabecera)
        tuplas_malas = []
        for comuna in comunas:
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE id = %s",
                (comuna[0],)
            )
            cuenta = cursor.fetchone()[0]
            if cuenta == 0:
                try:
                    SQL = f"INSERT INTO {tabla} (id, nombre, provincia, region) VALUES (%s, %s, %s, %s)"
                    data = (comuna[0], comuna[1], comuna[2], comuna[3])
                    cursor.execute(SQL, data)
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    tuplas_malas += comuna
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Carga de Tupla:", comuna)
            else:
                print(f"Comuna {comuna[0]}, {comuna[1]} ya existe")
        print(tuplas_malas)

        

# Conexión a la base de datos
with psycopg2.connect(
    host= DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_USER_PASSWORD,
    port=DATABASE_PORT,
    database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = ('IIC2413-Entrega-2/data/comuna.csv')
            nombre_tabla = 'comunas'
            carga_comuna(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")