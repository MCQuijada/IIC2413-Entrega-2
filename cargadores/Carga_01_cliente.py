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

def encriptador(key, contraseña):
    lista_caracteres = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    contraseña_encriptada = ''
    for caracter in contraseña:
        index = lista_caracteres.index(caracter)
        contraseña_encriptada += key[index]
    return contraseña_encriptada

def descencriptador(key, constraseña_encriptada):
    lita_caracteres = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    contraseña = ''
    for caracter in constraseña_encriptada:
        index = key.index(caracter)
        contraseña += lita_caracteres[index]
    return contraseña

def carga_cliente(archivo_csv, tabla, cursor):
    key=['!', ':', '5', 'Y', '=', 'k', '8', 'F', '4', '*', ' ',
        '?', '+', '&', ')', 'S', '.', 'R', 'V', 't', 'Z', 'f', 'n', 
        '1', 'a', 'A', '@', 'p', 'K', 'e', 'D', ';', 'v', '`', 'J', 
        '<', '7', "'", 'N', 'c', 'm', '}', 'H', 'd', 'I', 'g', 'P', 
        '(', '6', 'x', 'U', 'h', 'u', ',', 'w', 'X', '-', '{', 'C', 
        '$', 'r', 's', '/', 'z', 'M', 'E', '~', 'j', 'q', 'B', '>', 
        'b', '|', 'Q', '[', '^', '9', '"', 'L', 'i', '#', '0', 'W', 
        '_', 'y', 'o', 'T', '2', 'l', '\\', 'O', '%', '3', ']', 'G']
    
    with open(archivo_csv, 'r') as f:
        Clientes = csv.reader(f, delimiter=';')
        next(Clientes)  # me salto la primera fila (cabecera)
        tuplas_malas = []
        for cliente in Clientes:
            if True:
                try:
                    cliente[3] = encriptador(key, cliente[3])
                    SQL = f"INSERT INTO {tabla} (nombre, email, clave, fono) VALUES (%s, %s, %s, %s)"
                    data = ( cliente[0], cliente[1], cliente[3], cliente[2],)
                    cursor.execute(SQL, data)
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    tuplas_malas.append((error,data))
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Una carga lista", cliente[1])
    print('tuplas malas:')
    for mala in tuplas_malas:
        print(mala)
        print(" ")

# Conexión a la base de datos


with psycopg2.connect(
        host= DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_USER_PASSWORD,
        port=DATABASE_PORT,
        database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = ('IIC2413-Entrega-2/data/clientes.csv')
            nombre_tabla = 'clientes'
            carga_cliente(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")