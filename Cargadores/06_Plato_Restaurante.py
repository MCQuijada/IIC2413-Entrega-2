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
                    cursor.execute(
                        f"INSERT INTO {tabla} (id_plato, id_restaurante) VALUES (%s, %s)",
                        (resultado[0], resultado[1])
                    )
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
archivo_csv = 'platos.csv'
nombre_tabla = 'PlatosRestaurantes'  # Asumí que esta es la tabla destino correcta
carga_plato_restaurante(archivo_csv, nombre_tabla, cur)
cur.close()
conn.close()
