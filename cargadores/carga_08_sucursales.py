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

def carga_sucursales(archivo_csv, tabla, cursor, conn):
    malas = []
    with open(archivo_csv, mode='r', encoding='mac_roman') as f:
        datos = csv.reader(f, delimiter=';')
        next(datos)  # me salto la primera fila (cabecera)
        for dato in datos:
            cursor.execute(
                "SELECT id FROM Restaurantes WHERE nombre = %s",
                (dato[0],)
            )
            row = cursor.fetchone()
            direccion = dato[5].split(',')
            comuna = direccion.pop(1).lstrip()
            direccion = ','.join(direccion).strip()
            cursor.execute(
                '''SELECT id FROM Comunas WHERE nombre = %s''',
                (comuna,)
            )
            id_comuna = cursor.fetchone()
            if row and id_comuna:
                id_restaurante = row[0]
                id_comuna = id_comuna[0]
                try:
                    SQL = f"INSERT INTO {tabla} (id_restaurante, sucursal, direccion, fono, id_comuna) VALUES (%s, %s, %s, %s, %s)"
                    data = (id_restaurante, dato[4], direccion, dato[6], id_comuna,)
                    print(data)
                    cursor.execute(SQL, data)
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback en caso de error
                    malas.append(data)
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Dato Guardado:", data)
            else:
                malas.append(dato)
    print("Malas")
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
            archivo_csv = os.path.join(dir_actual,'data','restaurantes2.csv')
            nombre_tabla = 'sucursales'
            carga_sucursales(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")
