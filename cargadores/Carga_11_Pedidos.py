import csv
import psycopg2
import datetime

from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_USER_PASSWORD = os.getenv('DATABASE_USER_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')

def carga_pedido(archivo_csv, nombre_tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f, delimiter=";")
        next(datos)
        malas = []
        for dato in datos:
            print(dato)
            cursor.execute(
                '''SELECT Clientes.id, Deliverys.id, Despachadores.id 
                FROM Clientes, Deliverys, Despachadores
                WHERE Clientes.email = %s AND Deliverys.nombre = %s AND Despachadores.nombre = %s''',
                (dato[1], dato[2], dato[3])
            )
            row = cursor.fetchall()
            print(row)
            if row:
                id_cliente, id_delivery, id_despachador = row[0]
                fecha = datetime.datetime.strptime(dato[5], "%d-%m-%y").date()
                hora = datetime.datetime.strptime(dato[6], "%H:%M:%S").time()
                try:
                    SQL = f"INSERT INTO {nombre_tabla} (id, id_cliente, id_delivery, id_despachador, fecha, hora, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    data = (dato[0], id_cliente, id_delivery, id_despachador, fecha, hora, dato[7],)
                    print(data)

                    cursor.execute(SQL, data)
                except Exception as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                    malas.append((error,dato))
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Datos guardados:", dato)
            else:
                malas.append(("TUPLAS NO ENCONTRADAS",dato))
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
            archivo_csv = ('IIC2413-Entrega-2/data/pedidos2.csv')
            nombre_tabla = 'pedidos'
            carga_pedido(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")
