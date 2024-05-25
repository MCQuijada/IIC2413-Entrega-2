import csv
import psycopg2

def carga_restaurantes(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Restaurantes = csv.reader(f)
        next(Restaurantes)  # me salto la primera fila (cabecera)
        for restaurant in Restaurantes:
            try:
                SQL = f"INSERT INTO {tabla} (id, nombre, vigencia, estilo, repartoming) VALUES (%s, %s, %s, %s, %s)"
                data = (id, restaurant[0], restaurant[1], restaurant[2], restaurant[3],)
                cursor.execute(SQL, data)
                id += 1
            except psycopg2.IntegrityError as error:
                print(f"Error de integridad: {error}")
                conn.rollback()  # Rollback para evitar transacciones inconsistentes
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
            archivo_csv = 'restaurantes.csv'
            nombre_tabla = 'Restaurantes'
            carga_restaurantes(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
