import csv
import psycopg2
import datetime

def carga_suscripciones(archivo_csv, tabla, cursor):
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
                    SQL = f"INSERT INTO {tabla} (id, id_cliente, id_delivery, ultimo_pago, estado, fecha, ciclo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    data = (id, ids[0], ids[1], dato[3], dato[4], fecha, dato[5],)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as Error:
                    print(f"Error de integridad: {Error}")
                    conn.rollback()  # Rollback en caso de error
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
            archivo_csv = 'suscripciones.csv'
            nombre_tabla = 'Suscripciones'
            carga_suscripciones(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
