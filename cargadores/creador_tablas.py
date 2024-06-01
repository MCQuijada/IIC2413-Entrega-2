#Cambios
#Email 45
#Direccion text
#Comuna 50
#platos| sin tiempo, porciones, precio - nombre 40 - Pescado en Salsa de Mantequilla
#platos_restaurantes -> con tiempo, porciones y precio
#CADA RESTAURANTE OFRECE EL PLATO DE SOLO UNA FORMA.

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_USER_PASSWORD = os.getenv('DATABASE_USER_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')

def creador_de_tablas(SQL, cursor, tabla):
    try:
        cursor.execute(SQL)
    except Exception as Error:
        print(f"Error al crear la tabla {tabla}: {Error} ")


SQL_1_clientes = '''
    CREATE TABLE IF NOT EXISTS clientes(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL,
        email VARCHAR(45) NOT NULL UNIQUE,
        clave VARCHAR(100) NOT NULL,
        fono VARCHAR(12) NOT NULL
    );
'''
SQL_2_comunas = '''
    CREATE TABLE IF NOT EXISTS comunas(
        id INT PRIMARY KEY,
        nombre VARCHAR(30),
        provincia VARCHAR(30),
        region VARCHAR(50)
    );
'''

SQL_3_direcciones = '''
    CREATE TABLE IF NOT EXISTS direcciones(
        id SERIAL PRIMARY KEY,
        direccion TEXT NOT NULL UNIQUE,
        cut_comuna INT,
        FOREIGN KEY (cut_comuna) REFERENCES comunas(id)
    );
'''

SQL_3_5_direccion_cleinte = '''
    CREATE TABLE IF NOT EXISTS direcciones_clientes(
    id_direccion INT,
    id_cliente INT,
    PRIMARY KEY(id_direccion, id_cliente),
    FOREIGN KEY (id_direccion) REFERENCES direcciones(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    )
'''

SQL_4_restaurantes = '''
    CREATE TABLE IF NOT EXISTS restaurantes(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL UNIQUE,
        vigencia BOOLEAN NOT NULL,
        estilo VARCHAR(30) NOT NULL,
        repartoming INT
    );
'''

SQL_5_platos = '''
    CREATE TABLE IF NOT EXISTS platos(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(40) NOT NULL UNIQUE,
        descripcion TEXT,
        estilo VARCHAR(30) NOT NULL,
        restriccion VARCHAR(30),
        ingredientes TEXT
        );
'''


SQL_6_platos_restaurantes = '''
    CREATE TABLE IF NOT EXISTS platos_restaurantes(
        id INT PRIMARY KEY,
        id_plato INT,
        id_restaurante INT,
        disponibilidad BOOLEAN NOT NULL,
        porciones INT DEFAULT 1 CHECK (porciones >= 1),
        precio INT NOT NULL,
        tiempo_prep INT DEFAULT 5 CHECK (tiempo_prep >= 1 AND tiempo_prep <= 60),
        FOREIGN KEY (id_plato) REFERENCES platos(id),
        FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id)
    );
'''

SQL_7_sucursales = '''
    CREATE TABLE IF NOT EXISTS sucursales(
            id Serial UNIQUE,
            id_restaurante INT,
            sucursal VARCHAR(30) NOT NULL,
            direccion TEXT NOT NULL,
            fono VARCHAR(12) NOT NULL,
            id_comuna INT,
            FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
            FOREIGN KEY (id_comuna) REFERENCES comunas(id),
            PRIMARY KEY(direccion, id_restaurante)
    );
'''

SQL_8_deliverys = '''
    CREATE TABLE IF NOT EXISTS deliverys(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL UNIQUE,
        vigencia BOOLEAN NOT NULL,
        fono VARCHAR(12) NOT NULL UNIQUE,
        tiempo_despacho INT NOT NULL,
        precio_unitario INT,
        precio_mensual INT CHECK (precio_mensual <= 4*precio_unitario),
        precio_anual INT CHECK (precio_mensual <= 12*precio_mensual)
    );
'''

SQL_9_suscripciones = '''
    CREATE TABLE IF NOT EXISTS suscripciones(
        id SERIAL,
        id_cliente INT,
        id_delivery INT,
        ultimo_pago INT,
        estado VARCHAR(30),
        fecha DATE,
        ciclo VARCHAR(30),
        PRIMARY KEY (id_cliente, id_delivery),
        FOREIGN KEY (id_cliente) REFERENCES clientes(id),
        FOREIGN KEY (id_delivery) REFERENCES deliverys(id)
    );
'''

SQL_10_despachadores = '''
    CREATE TABLE IF NOT EXISTS despachadores(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL,
        fono VARCHAR(12) NOT NULL UNIQUE
    );
'''

SQL_11_pedidos = '''
    CREATE TABLE IF NOT EXISTS pedidos(
        id INT PRIMARY KEY,
        id_cliente INT,
        id_delivery INT,
        id_despachador INT,
        fecha DATE NOT NULL,
        hora TIME,
        estado VARCHAR(30),
        FOREIGN KEY (id_cliente) REFERENCES clientes(id),
        FOREIGN KEY (id_delivery) REFERENCES deliverys(id),
        FOREIGN KEY (id_despachador) REFERENCES despachadores(id)
    );
'''

SQL_12_calificaciones = '''
    CREATE TABLE IF NOT EXISTS calificaciones(
        id_pedido INT PRIMARY KEY,
        cal_cliente INT CHECK (cal_cliente >= 1 AND cal_cliente <= 5),
        cal_despachador INT CHECK (cal_despachador >= 1 AND cal_despachador <= 5),
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id)
    );
'''

SQL_13_pedidos_platos = '''
    CREATE TABLE  IF NOT EXISTS pedidos_platos(
        id_pedido INT,
        id_plato INT,
        id_sucursal INT,
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id),
        FOREIGN KEY (id_plato) REFERENCES platos_restaurantes(id),
        PRIMARY KEY (id_pedido, id_plato)
    );
'''
##### NO VA
SQL_14_sucursales_comunas = '''
    CREATE TABLE IF NOT EXISTS sucursales_comunas(
        id_sucursal INT,
        id_comuna INT,
        FOREIGN KEY (id_sucursal) REFERENCES sucursales(id),
        FOREIGN KEY (id_comuna) REFERENCES comunas(id),
        PRIMARY KEY (id_sucursal, id_comuna)     
    );
'''

SQL_15_ingredientes = '''
    CREATE TABLE IF NOT EXISTS ingredientes(
        id INT PRIMARY KEY,
        ingrediente VARCHAR(30) NOT NULL
    );
'''

SQL_16_plato_ingredientes = '''
    CREATE TABLE IF NOT EXISTS plato_ingredientes(
        id_plato INT,
        id_ingrediente INT,
        FOREIGN KEY (id_plato) REFERENCES platos(id),
        FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id),
        PRIMARY KEY (id_plato, id_ingrediente)
    );
'''

instrucciones_de_tablas = [
    SQL_1_clientes, SQL_2_comunas, SQL_3_direcciones, SQL_3_5_direccion_cleinte, SQL_4_restaurantes, SQL_5_platos, SQL_6_platos_restaurantes,
    SQL_7_sucursales, SQL_8_deliverys, SQL_9_suscripciones, SQL_10_despachadores, SQL_11_pedidos,
    SQL_12_calificaciones, SQL_13_pedidos_platos, SQL_14_sucursales_comunas, SQL_15_ingredientes, SQL_16_plato_ingredientes
]
nombres_de_tablas = ['clientes', 'comunas', 'direcciones', 'direccion_cliente', 
                     'restaurantes', 'platos', 'platos_restaurantes', 
                     'sucursales', 'deliverys', 'suscripciones', 
                     'despachadores', 'pedidos', 'calificaciones',
                     'pedidos_platos', 'sucursales_comunas', 'ingredientes', 
                     'plato_ingredientes']

tablas_nombre_instruccion = list(zip(nombres_de_tablas, instrucciones_de_tablas))

try:
    with psycopg2.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_USER_PASSWORD,
        port=DATABASE_PORT,
        database=DATABASE_NAME
    ) as conn:
        with conn.cursor() as cur:
            for nombre_tabla, instruccion_tabla in tablas_nombre_instruccion:
                creador_de_tablas(instruccion_tabla, cur, nombre_tabla)
                print(f"Carga Finalizada de {nombre_tabla}")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")