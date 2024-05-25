import csv
import psycopg2

def carga_plato_restaurante(archivo_csv, tabla, cursor):
    with open(archivo_csv, 'r') as f:
        Platos = csv.reader(f)
        next(Platos)  # Saltar la primera fila (cabecera)
        for plato in Platos:
            cursor.execute(
                "SELECT Platos.id, Restaurantes.id FROM Restaurantes, Platos WHERE Platos.nombre = %s AND Restaurantes.nombre = %s",
                (plato[1], plato[10])
            )
            resultado = cursor.fetchone()

            if resultado:
                try:
                    SQL = f"INSERT INTO {tabla} (id_plato, id_restaurante) VALUES (%s, %s)"
                    data = (resultado[0], resultado[1],)
                    cursor.execute(SQL, data)
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
            archivo_csv = 'platos.csv'
            nombre_tabla = 'Platos_Restaurantes'
            carga_plato_restaurante(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
