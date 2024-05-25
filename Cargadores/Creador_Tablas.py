import psycopg2

def creador_de_tablas(SQL, cursor, tabla):
    try:
        cursor(SQL)
    except Exception as Error:
        print(f"Error al creal la tabla {tabla}: {Error} ")


SQL_1_Clientes = '''
    CREATE TABLE IF NOT EXISTS Clientes(
        id INT PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL,
        email VARCHAR(30) NOT NULL UNIQUE,
        clave VARCHAR(100) NOT NULL,
        fono VARCHAR(12) NOT NULL
    );
'''
SQL_2_Comunas = '''
    CREATE TABLE IF NOT EXISTS Comunas(
        id INT PRIMARY KEY,
        nombre VARCHAR(30),
        provincia VARCHAR(30),
        region VARCHAR(30)
    );
'''

SQL_3_Direcciones = '''
    CREATE TABLE IF NOT EXISTS Direcciones(
        id INT PRIMARY KEY,
        id_cliente INT,
        direccion VARCHAR(30) NOT NULL,
        cut_comuna INT,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
        FOREIGN KEY (cut_comuna) REFERENCES Comunas(id)
    );
'''

SQL_4_Restaurantes = '''
    CREATE TABLE IF NOT EXISTS restaurantes(
        id INT PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL UNIQUE,
        vigencia BOOLEAN NOT NULL,
        estilo VARCHAR(30) NOT NULL,
        repartoming INT
    );
'''

SQL_5_Platos = '''
    CREATE TABLE IF NOT EXISTS Platos(
        id INT PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL UNIQUE,
        descripcion TEXT,
        disponibilidad BOOLEAN NOT NULL,
        estilo VARCHAR(30) NOT NULL,
        restriccion INT,
        ingredientes TEXT,
        porciones INT DEFAULT 1 CHECK (id >= 1),
        precio INT NOT NULL,
        tiempo_prep INT DEFAULT 5 CHECK (tiempo_prep >= 1 AND tiempo_prep <= 60),
    );
'''

SQL_6_Plato_Restaurante = '''
    CREATE TABLE IF NOT EXISTS Platos_restaurantes(
        id_plato INT,
        id_restaurante INT,
        FOREIGN KEY (id_plato) REFERENCES Platos(id),
        FOREIGN KEY (id_restaurante) REFERENCES Restaurantes(id)
);
'''

SQL_7_Sucursales = '''
    CREATE TABLE IF NOT EXISTS sucursales(
            id INT PRIMARY KEY,
            id_restaurante INT FOREIGN KEY,
            sucursal VARCHAR(30) NOT NULL,
            direccion VARCHAR(30) NOT NULL,
            fonos VARCHAR(12) NOT NULL,
            id_comuna INT FOREIGN KEY
    );
'''

SQL_8_Deliverys = '''
    CREATE TABLE IF NOT EXISTS Deliverys(
        id INT PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL,
        vigencia BOOLEAN NOT NULL,
        fono VARCHAR(12) NOT NULL UNIQUE,
        tiempo_despacho INT NOT NULL,
        precio_unitario INT,
        precio_mensual INT CHECK (precio_mensual <= 4*precio_unitario),
        precio_anual INT CHECK (precio_mensual <= 12*precio_mensual)
    );
'''

SQL_9_Suscripciones = '''
    CREATE TABLE IF NOT EXISTS Suscripciones(
        id INT PRIMARY KEY,
        id_cliente INT,
        id_delivery INT,
        ultimo_pago INT,
        estado VARCHAR(30),
        fecha DATE,
        ciclo VARCHAR(30),
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
        FOREIGN KEY (id_delivery) REFERENCES Deliverys(id)
    );
'''

SQL_10_Despachadores = '''
    CREATE TABLE IF NOT EXISTS Despachadores(
        id INT PRIMARY KEY,
        nombre VARCHAR(30) NOT NULL,
        fono VARCHAR(12) NOT NULL
    );
'''

SQL_11_Pedidos = '''
    CREATE TABLE IF NOT EXISTS Pedidos(
        id INT PRIMARY KEY,
        id_cliente INT,
        id_sucursal INT,
        id_delivery INT,
        id_despachador INT,
        fecha DATE NOT NULL,
        hora TIME,
        estado VARCHAR(30),
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
        FOREIGN KEY (id_sucursal) REFERENCES Sucursales(id),
        FOREIGN KEY (id_delivery) REFERENCES Deliverys(id),
        FOREIGN KEY (id_despachador) REFERENCES Despachadores(id)
    );
'''

SQL_12_Calificaciones = '''
    CREATE TABLE IF NOT EXISTS Calificaciones(
        id INT PRIMARY KEY,
        id_pedido INT,
        cal_cliente INT CHECK (cal_cliente >= 1 AND cal_cliente <= 5),
        cal_despachador INT CHECK (cal_despachador >= 1 AND cal_despachador <= 5),
        FOREIGN KEY (id_pedido) REFERENCES Pedidos(id)
    );
'''

SQL_13_Pedidos_Platos = '''
    CREATE TABLE  IF NOT EXISTS pedidos_platos(
        id_pedido INT,
        id_plato INT,
        FOREIGN KEY (id_pedido) REFERENCES Pedidos(id),
        FOREIGN KEY (id_plato) REFERENCES Platos(id)
    );
'''

lista_de_tablas = [
    SQL_1_Clientes, SQL_2_Comunas, SQL_3_Direcciones, SQL_4_Restaurantes, SQL_5_Platos, SQL_6_Plato_Restaurante,
    SQL_7_Sucursales, SQL_8_Deliverys, SQL_9_Suscripciones, SQL_10_Despachadores, SQL_11_Pedidos,
    SQL_12_Calificaciones, SQL_13_Pedidos_Platos
]

try:
    with psycopg2.connect(
        host="pavlov.ing.puc.cl",
        user="grupo121",
        password="bases202401",
        port="5432",
        database="Proyecto_Base_Datos"
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = 'datos.csv'
            nombre_tabla = 'nombre_tabla'
            carga_restaurantes(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")