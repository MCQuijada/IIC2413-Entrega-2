#NO la hice
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

def carga_direccion_cliente(archivo_csv, tabla,cursor, conn):
    with open(archivo_csv, 'r') as f:
        clientes = csv.reader(f, delimiter=';')
        next(clientes)  # me salto la primera fila (cabecera)
        tuplas_malas = []
        for cliente in clientes:
            cursor.execute(
                "SELECT clientes.id FROM clientes WHERE clientes.email = %s",
                (cliente[1], )
            )
            cliente_id = cursor.fetchone()
            cursor.execute(
                "SELECT direcciones.id FROM direcciones WHERE direcciones.direccion = %s",
                (cliente[4], )
            )
            direccion_id = cursor.fetchone()
            if cliente_id and direccion_id:
                cliente_id = cliente_id[0]
                direccion_id = direccion_id[0]
                print(cliente_id,direccion_id)
            else:
                tuplas_malas.append(cliente[0],cliente(4))
                continue
            try:
                SQL = f"INSERT INTO {tabla} (id_direccion, id_cliente) VALUES (%s, %s)"
                data = (direccion_id, cliente_id,)
                print("DATA:", data)
                cursor.execute(SQL, data)
            except Exception as error:
                if not isinstance(error, psycopg2.IntegrityError) and error.pgcode == '23505':
                    print(f"Error de integridad: {error}")
                    tuplas_malas.append(data)
                conn.rollback()  # Rollback para evitar transacciones inconsistentes
            else:
                conn.commit()  # Commit para guardar los cambios
                print("Tupla guardada:", data)
    print("MALAS: ",tuplas_malas)

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
            archivo_csv = os.path.join(dir_actual,'data','clientes.csv')
            nombre_tabla = 'direcciones_clientes'
            carga_direccion_cliente(archivo_csv, nombre_tabla, cur, conn)
            print("Carga Finalizada")