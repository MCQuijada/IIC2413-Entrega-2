import csv
import os
import psycopg2

def carga_calificaciones(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Datos = csv.reader(f)
        next(Datos)  # me salto la primera fila (cabecera)
        for dato in Datos:
            if True:
                try:
                    SQL = f"INSERT INTO {tabla} (id, id_pedido, cal_cliente, cal_despachador) VALUES (%s, %s, %s, %s)"
                    data = (id, dato[0], dato[1], dato[3],)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
            else:
                print(f"Cliente {cliente[1]} ya existe")

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
            archivo_csv = os.path.join('..','data','calificaciones.csv')
            nombre_tabla = 'Calificaciones'
            carga_calificaciones(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")