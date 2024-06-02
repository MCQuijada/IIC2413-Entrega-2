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

def carga_despachador(archivo_csv, tabla, cursor, conn):
    malas = []
    with open(archivo_csv, 'r') as f:
        Datos = csv.reader(f, delimiter=";")
        next(Datos)  # me salto la primera fila (cabecera)
        for dato in Datos:
            if True:
                try:
                    SQL = f"INSERT INTO {tabla} (nombre, fono) VALUES (%s, %s)"
                    data = (dato[11], dato[12],)
                    cursor.execute(SQL, data)
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    malas.append(("ERROR",error,data))
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("DATO GUARDADO:", data)
    print("MALAS:")
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
            archivo_csv = os.path.join('..','data','cldeldes.csv')
            nombre_tabla = 'despachadores'
            carga_despachador(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")