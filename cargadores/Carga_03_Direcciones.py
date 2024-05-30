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
    id = 1  # para los id
    tuplas_malas = []
    i = 0
    with open(archivo_csv, 'r') as f:
        Direcciones = csv.reader(f, delimiter=';')
        next(Direcciones)  # me salto la primera fila (cabecera)
        for direccion in Direcciones:
            if len(direccion) < 6:
                cliente = [elem1 + elem2 for elem1, elem2 in zip(direccion[i], direccion[i+1])]
                print("Tupla Arreglada:", direccion)
                if len(cliente) > 6:
                    tuplas_malas += Clientes[i]
                    continue
            cursor.execute(
                '''SELECT id FROM Clientes
                WHERE Clientes.email = %s''',
                (direccion[1],)
            )
            cliente = cursor.fetchone()
            if cliente:            
                try:
                    SQL = f"INSERT INTO {tabla} (id, id_cliente, direccion, cut_comuna) VALUES (%s, %s, %s, %s)"
                    data = (id, cliente[0] , direccion[4], direccion[5],)
                    cursor.execute(SQL, data)
                    id += 1
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                    tuplas_malas += direccion
                else:
                    conn.commit()  # Commit para guardar los cambios
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
            archivo_csv = ('data/clientes.csv')
            nombre_tabla = 'direcciones'
            carga_direcciones(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")
