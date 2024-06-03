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

def carga_suscripciones(archivo_csv, tabla, cursor, conn):
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f, delimiter=';')
        next(datos)  # me salto la primera fila (cabecera)
        malas = []
        repetidas = []
        for dato in datos:
            cursor.execute(
                "SELECT clientes.id, deliverys.id FROM clientes, deliverys WHERE Clientes.email = %s AND Deliverys.nombre = %s",
                (dato[0], dato[1])
            )
            row = cursor.fetchone()
            if row:
                ids = row
                fecha = datetime.datetime.strptime(dato[4], "%d-%m-%y").date()
                try:
                    SQL = f"INSERT INTO {tabla} (id_cliente, id_delivery, ultimo_pago, estado, fecha, ciclo) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = (ids[0], ids[1], dato[3], dato[2], fecha, dato[5],)
                    cursor.execute(SQL, data)
                except psycopg2.IntegrityError as error:
                    if not isinstance(error, psycopg2.IntegrityError) and error.pgcode == '23505':
                        print(f"Error de integridad: {error}")
                        malas.append(("Mala: ",error,"\n",dato))
                    else:
                        repetidas.append(dato)
                    conn.rollback()  # Rollback en caso de error
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Datos Cargados: ", data)
            else:
                malas.append(("NO ESTA:",dato))
    for m in malas:
        print("MALA: ",m)
    print("----------------------------")
    print("----------------------------")
    for r in repetidas:
        print("Repetida",r)

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
            archivo_csv = os.path.join(dir_actual,'data','suscripciones.csv')
            nombre_tabla = 'suscripciones'
            carga_suscripciones(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")

