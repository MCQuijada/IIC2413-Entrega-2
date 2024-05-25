import csv
import psycopg2

def carga_comuna(archivo_csv, tabla, cursor):
    with open(archivo_csv, 'r') as f:
        comunas = csv.reader(f)
        next(comunas)  # me salto la primera fila (cabecera)
        for comuna in comunas:
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE id = %s",
                (comuna[0],)
            )
            cuenta = cursor.fetchone()[0]
            if cuenta == 0:
                try:
                    SQL = f"INSERT INTO {tabla} (id, nombre, provincia, region) VALUES (%s, %s, %s, %s)"
                    data = (comuna[0], comuna[1], comuna[2], comuna[3])
                    cursor.execute(SQL, data)
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
            else:
                print(f"Comuna {comuna[0]}, {comuna[1]} ya existe")

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
            archivo_csv = 'comuna.csv'
            nombre_tabla = 'Comunas'
            carga_comuna(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
