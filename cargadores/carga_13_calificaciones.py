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

def carga_calificaciones(archivo_csv, tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        malas = []
        Datos = csv.reader(f, delimiter=";")
        next(Datos)  # me salto la primera fila (cabecera)
        for dato in Datos:
            if True:
                try:
                    SQL = f"INSERT INTO {tabla} (id_pedido, cal_cliente, cal_despachador) VALUES (%s, %s, %s)"
                    data = (dato[0], dato[1], dato[2],)
                    cursor.execute(SQL, data)
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                    malas.append((error,dato))
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("DATOS GUARDADOS:", dato)
    print("MALAS")
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
            dir_actual = os.getcwd()
            archivo_csv = os.path.join(dir_actual,'data','calificacion.csv')
            nombre_tabla = 'calificaciones'
            carga_calificaciones(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")