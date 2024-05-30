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

def carga_delivery(tabla_csv, tabla, cursor, conn):
    with open(tabla_csv, 'r') as f:
        cedeldes = csv.reader(f, delimiter=';')
        next(cedeldes)
        malas = []
        for dato in cedeldes:
            try:
                SQL = f"INSERT INTO {tabla} (nombre, vigencia, fono, tiempo_despacho, precio_unitario, precio_mensual, precio_anual) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
                data = (dato[4],dato[5],dato[6],dato[7],dato[8], dato[9], dato[10],)
                cursor.execute(SQL, data)
            except Exception as error:
                if not isinstance(error, psycopg2.IntegrityError) and error.pgcode == '23505':
                    print(f"Error de integridad: {error}")
                    malas += dato
                conn.rollback()
            else:
                conn.commit()  # Commit para guardar los cambios
                print("Tupla Cargada:", data)
    print("MALAS: ",malas)
                 


with psycopg2.connect(
    host= DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_USER_PASSWORD,
    port=DATABASE_PORT,
    database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = ('IIC2413-Entrega-2/data/cldeldes.csv')
            nombre_tabla = 'deliverys'
            carga_delivery(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")