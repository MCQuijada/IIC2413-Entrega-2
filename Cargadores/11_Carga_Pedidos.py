import csv
import psycopg2
import datetime

def carga_pedido(archivo_csv, nombre_tabla, cursor):
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f)
        next(datos)  # me salto la primera fila (cabecera)
        for dato in datos:
            cursor.execute(
                '''SELECT Clientes.id, Deliverys.id, Despachadores.id 
                FROM Clientes, Deliverys, Despachadores
                WHERE Clientes.email = %s AND Deliverys.nombre = %s AND Despachadores.nombre = %s''',
                (dato[1], dato[2], dato[3])
            )
            row = cursor.fetchone()
            if row:
                id_cliente, id_delivery, id_despachador = row
                fecha = datetime.datetime.strptime(dato[5], "%d-%m-%y").date()
                hora = datetime.datetime.strptime(dato[6], "%H:%M:%S").time()
                try:
                    SQL = f"INSERT INTO {nombre_tabla} (id, id_cliente, id_sucursal, id_delivery, id_despachador, fecha, hora, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (dato[0], id_cliente, 1, id_delivery, id_despachador, fecha, hora, dato[7],)
                    cursor.execute(SQL, data)
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios

# Conexión a la base de datos
try:
    with psycopg2.connect(
        host="pavlov.ing.puc.cl",
        user="grupo121",
        password="bases202401",
        port="5432",
        database="Proyecto_Base_Datos"
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = 'pedidos2.csv'
            nombre_tabla = 'Pedidos'
            carga_pedido(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
