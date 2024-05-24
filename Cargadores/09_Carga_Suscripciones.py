import csv
import psycopg2
import datetime

def carga_tabla(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f)
        next(datos)  # me salto la primera fila (cabecera)
        for dato in datos:
            cursor.execute(
                "SELECT cliente.id, delivery.id FROM Clientes, Deliverys WHERE Clientes.email = %s AND Deliverys.nombre = %s",
                (dato[0], dato[1])
            )
            row = cursor.fetchone()
            if row:
                ids = row
                fecha = datetime.datetime.strptime(dato[2], "%d-%m-%y").date()
                try:
                    cursor.execute(
                        f"INSERT INTO {tabla} (id, id_cliente, id_delivery, ultimo_pago, estado, fecha, ciclo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (id, ids[0], ids[1], dato[3], dato[4], fecha, dato[5])
                    )
                    id += 1
                except psycopg2.IntegrityError as Error:
                    print(f"Error de integridad: {Error}")
                    conn.rollback()  # Rollback en caso de error
                else:
                    conn.commit()  # Commit para guardar los cambios

# Conexión a la base de datos
conn = psycopg2.connect(
    user="tu_usuario",
    password="tu_contraseña",
    host="localhost",
    port="5432",
    database="Proyecto_Base_Datos"
)

cur = conn.cursor()
archivo_csv = 'nombre_del_archivo.csv'
nombre_tabla = 'nombre_de_la_tabla'
carga_tabla(archivo_csv, nombre_tabla, cur)
cur.close()
conn.close()
