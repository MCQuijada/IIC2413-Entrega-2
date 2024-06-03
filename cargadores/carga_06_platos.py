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

def carga_platos(archivo_csv, tabla, cursor, conn):
    tupla_mala = []
    with open(archivo_csv, 'r') as f:
        Platos = csv.reader(f,delimiter=';')
        next(Platos)  # me salto la primera fila (cabecera)
        for plato in Platos:
            try:
                SQL = f"INSERT INTO {tabla} (nombre, descripcion, estilo, restriccion, ingredientes) VALUES (%s, %s, %s, %s, %s)"
                data = (plato[1], plato[2], plato[4], plato[5], plato[6],)
                cursor.execute(SQL, data)
            except Exception as error:
                if not isinstance(error, psycopg2.IntegrityError):
                    print(f"Error de integridad: {error}")
                    tupla_mala.append(data)
                conn.rollback()  # Rollback para evitar transacciones inconsistentes
            else:
                conn.commit()  # Commit para guardar los cambios
                print("DATOS GUARDADOS:", data)
    print("----Malas-----\n")
    for mala in tupla_mala:
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
            archivo_csv = os.path.join(dir_actual,'data','platos.csv')
            nombre_tabla = 'platos'
            carga_platos(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")