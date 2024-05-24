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
            if row:
                id_restaurante = row[0]
                try:
                    cursor.execute(
                        f"INSERT INTO {tabla} (id, id_restaurante, sucursal, direccion, fonos) VALUES (%s, %s, %s, %s, %s)",
                        (id, id_restaurante, dato[5], dato[6], dato[7])
                    )
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
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
archivo_csv = 'restaurantes.csv'
nombre_tabla = 'RestaurantesSucursal'  # Nombre de la tabla destino
carga_restaurantes(archivo_csv, nombre_tabla, cur)
cur.close()
conn.close()
