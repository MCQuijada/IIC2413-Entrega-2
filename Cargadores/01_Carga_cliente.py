import csv
import psycopg2

def carga_direccion(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Clientes = csv.reader(f)
        next(Clientes)  # me salto la primera fila (cabecera)
        for cliente in Clientes:
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE email = %s",
                (cliente[1],)
            )
            cuenta = cursor.fetchone()[0]
            if cuenta == 0:
                try:
                    cursor.execute(
                        f"INSERT INTO {tabla} (id, nombre, email, clave, fono) VALUES (%s, %s, %s, %s, %s)",
                        (id, cliente[0], cliente[1], cliente[2], cliente[3])
                    )
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
            else:
                print(f"Cliente {cliente[1]} ya existe")

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
carga_direccion(archivo_csv, nombre_tabla, cur)

cur.close()
conn.close()
