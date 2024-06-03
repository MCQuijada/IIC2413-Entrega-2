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

def carga_pedidos_platos(archivo_csv, tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f, delimiter=";")
        next(datos)
        malas = []
        for dato in datos:
            platos_ids = dato[4].split()
            for id in platos_ids:
                cursor.execute(
                    "SELECT id FROM platos_restaurantes WHERE id = %s",
                    (id,)
                )
                row = cursor.fetchone()
                if row:
                    try:
                        SQL = f"INSERT INTO {tabla} (id_pedido, id_plato) VALUES (%s, %s)"
                        data = (dato[0], id,)
                        print(data)
                        cursor.execute(SQL, data)
                    except Exception as error:
                        print(f"Error de integridad: {error}")
                        conn.rollback()  # Rollback en caso de error
                        malas.append(data)
                    else:
                        conn.commit()  # Commit para guardar los cambios
                        print("Dato guardado:", data)
                else:
                    malas.append(("NO EXISTE",dato))
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
            archivo_csv = os.path.join('..','data','pedidos2.csv')
            nombre_tabla = 'pedidos_platos'
            carga_pedidos_platos(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")