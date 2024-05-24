import csv
import psycopg2

def carga_restaurantes(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Restaurantes = csv.reader(f)
        next(Restaurantes)  # me salto la primera fila (cabecera)
        for restaurant in Restaurantes:
            try:
                cursor.execute(
                    f"INSERT INTO {tabla} (id, nombre, vigencia, estilo, repartoming) VALUES (%s, %s, %s, %s, %s)",
                    (id, restaurant[0], restaurant[1], restaurant[2], restaurant[3])
                )
                id += 1
            except psycopg2.IntegrityError as error:
                print(f"Error de integridad: {error}")
                conn.rollback()  # Rollback para evitar transacciones inconsistentes
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
nombre_tabla = 'nombre_tabla'
carga_restaurantes(archivo_csv, nombre_tabla, cur)
cur.close()
conn.close()
