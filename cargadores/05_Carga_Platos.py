import csv
import psycopg2

def carga_platos(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Platos = csv.reader(f)
        next(Platos)  # me salto la primera fila (cabecera)
        for plato in Platos:
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE nombre = %s",
                (plato[1],)
            )
            cuenta = cursor.fetchone()[0]

            if cuenta == 0:
                try:
                    SQL = f"INSERT INTO {tabla} (id, nombre, descripcion, disponibilidad, estilo, restriccion, ingredientes, porciones, precio, tiempo_prep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (plato[0], plato[1], plato[2], plato[3], plato[4], plato[5], plato[6], plato[7], plato[8], plato[9],)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
            else:
                print(f"Plato {plato[1]} ya existe")

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
            archivo_csv = 'platos.csv'
            nombre_tabla = 'Platos'
            carga_platos(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")