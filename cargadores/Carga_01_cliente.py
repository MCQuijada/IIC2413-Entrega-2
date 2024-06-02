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

def carga_cliente(archivo_csv, tabla, cursor):
    with open(archivo_csv, 'r') as f:
        Clientes = csv.reader(f, delimiter=';')
        next(Clientes)  # me salto la primera fila (cabecera)
        tuplas_malas = []
        i = 0
        for cliente in Clientes:
            if len(cliente) < 6:
                print("tupla",cliente,"arreglada")
                cliente = [elem1 + elem2 for elem1, elem2 in zip(Clientes[i], Clientes[i+1])]
                if cliente > 6:
                    tuplas_malas += cliente
                    continue
                print("tupla",cliente,"arreglada")
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE email = %s",
                (cliente[1],)
            )
            cuenta = cursor.fetchone()[0]
            if cuenta == 0:
                try:
                    SQL = f"INSERT INTO {tabla} (nombre, email, clave, fono) VALUES (%s, %s, %s, %s)"
                    data = ( cliente[0], cliente[1], cliente[2], cliente[3],)
                    cursor.execute(SQL, data)
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    tuplas_malas += cliente
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Una carga lista", cliente[1])
            i += 1
    print('tuplas malas:', tuplas_malas)

# Conexión a la base de datos


with psycopg2.connect(
        host= DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_USER_PASSWORD,
        port=DATABASE_PORT,
        database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = os.path.join('..','data','clientes.csv')
            nombre_tabla = 'clientes'
            carga_cliente(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")






