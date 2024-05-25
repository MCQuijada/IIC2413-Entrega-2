import csv
import psycopg2

def carga_restaurantes(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f)
        next(datos)  # me salto la primera fila (cabecera)
        for dato in datos:
            cursor.execute(
                "SELECT id FROM Restaurantes WHERE nombre = %s",
                (dato[0],)
            )
            row = cursor.fetchone()
            direccion = dato[4].split(',')
            comuna = direccion.pop().strip()
            direccion = ','.join(direccion).strip()
            cursor.execute(
                '''SELECT id FROM Comunas WHERE nombre = %s''',
                (comuna,)
            )
            id_comuna = cursor.fetchone()[0]
            if row:
                id_restaurante = row[0]
                try:
                    SQL = f"INSERT INTO {tabla} (id, id_restaurante, sucursal, direccion, fono, id_comuna) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = (id, id_restaurante, dato[5], direccion, dato[7], id_comuna,)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
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
            archivo_csv = 'restaurante.csv'
            nombre_tabla = 'Sucursales'
            carga_restaurantes(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
