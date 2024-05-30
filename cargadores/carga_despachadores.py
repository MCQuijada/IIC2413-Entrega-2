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


def filtrar_datos_despachador():
    ruta_archivo = os.path.join('data','cldeldes.csv')
    despachadores = []

    with open(ruta_archivo, 'r', newline='') as archivo:
        csv_reader = csv.reader(archivo, delimiter=';')
        next(csv_reader)

        valores_despachador = set()
        for fila in csv_reader:
            nombre_despachador = fila[11]
            fono_despachador = fila[12]
            valores_despachador.add((nombre_despachador, fono_despachador))
        
        id_despachador = 0
        for nombre, fono in valores_despachador:
            despachadores.append((id_despachador, nombre, fono))
            id_despachador = id_despachador + 1

    return despachadores

def carga_despachador(cursor):
    ruta_archivo = os.path.join('..','data','cldeldes.csv')
    id = 1  # para los id
    with open(ruta_archivo, 'r') as f:
        datos = csv.reader(f)
        next(datos)  # me salto la primera fila (cabecera)
        for dato in datos:
            cursor.execute(
                f"SELECT COUNT(*) FROM despachadores WHERE email = %s",
                (dato[1],)
            )
            cuenta = cursor.fetchone()[0]
            if cuenta == 0:
                try:
                    SQL = f"INSERT INTO despachadores (id, nombre, fono) VALUES (%s, %s, %s)"
                    data = (id, dato[11], dato[12],)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    cursor.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    cursor.commit()  # Commit para guardar los cambios
            else:
                print(f"Cliente {dato[1]} ya existe")



for id, nombre, fono in filtrar_datos_despachador():
    print(id, nombre, fono)