import csv
import psycopg2

def carga_despachador(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Datos = csv.reader(f)
        next(Datos)  # me salto la primera fila (cabecera)
        for dato in Datos:
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE email = %s",
                (dato[1],)
            )
            cuenta = cursor.fetchone()[0]
            if cuenta == 0:
                try:
                    SQL = f"INSERT INTO {tabla} (id, nombre, fono) VALUES (%s, %s, %s)"
                    data = (id, dato[11], dato[12],)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
            else:
                print(f"Cliente {dato[1]} ya existe")

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
            archivo_csv = 'cldeldes.csv'
            nombre_tabla = 'Despachadores'
            carga_despachador(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")