import csv
import psycopg2

def carga_delivery(tabla_csv, tabla, cursor):
    id = 1 #para los id
    datos = tabla_csv.reader(tabla_csv)
    next(datos) #me salto lo primero
    for dato in datos:
        if True:
            try:
                SQL = f"INSERT INTO {tabla} VALUES (id, nombre, vigencia, fono, tiempo_despacho, precio_unitario, precio_mensual, precio_anual)" 
                data = (id, dato[4],dato[5],dato[6],dato[7],dato[8], dato[9], dato[10],)
                cursor.executable(SQL, data)
                id +=1
            except psycopg2.IntegrityError as Error:
                print(f"Error de integridad: {Error}")


try:
    with psycopg2.connect(
        host="pavlov.ing.puc.cl",
        user="grupo121",
        password="bases202401",
        port="5432",
        database="Proyecto_Base_Datos"
    ) as conn:
        with conn.cursor() as cur:
            archivo_csv = 'cldeldes.csv'
            nombre_tabla = 'Deliverys'
            carga_delivery(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")