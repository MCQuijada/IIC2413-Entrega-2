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
                    cursor.execute(
                        f"INSERT INTO {tabla} (id, nombre, provincia, region) VALUES (%s, %s, %s, %s)",
                        (comuna[0], comuna[1], comuna[2], comuna[3])
                    )
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
            else:
                print(f"Comuna {comuna[0]}, {comuna[1]} ya existe")

# Conexión a la base de datos
conn = psycopg2.connect(
    user="tu_usuario",
    password="tu_contraseña",
    host="localhost",
    port="5432",
    database="Proyecto_Base_Datos"
)

cur = conn.cursor()
archivo_csv = 'datos.csv'
nombre_tabla = 'nombre_tabla'
carga_comuna(archivo_csv, nombre_tabla, cur)

cur.close()
conn.close()
