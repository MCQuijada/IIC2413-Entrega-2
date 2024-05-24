import csv
import psycopg2
import datetime

def carga_tabla(archivo_csv, nombre_tabla, cursor):
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
                    cursor.execute(
                        f"INSERT INTO {nombre_tabla} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (dato[0], id_cliente, 1, id_delivery, id_despachador, fecha, hora, dato[7])
                    )
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios

# Conexión a la base de datos
conn = psycopg2.connect(
    user="nose",
    password="no se",
    host="nose",
    port="nose",
    database="xd"
)

cur = conn.cursor()
archivo_csv = '/ruta/al/archivo.csv'
nombre_tabla = 'nombre_de_tu_tabla'
carga_tabla(archivo_csv, nombre_tabla, cur)

cur.close()
conn.close()
