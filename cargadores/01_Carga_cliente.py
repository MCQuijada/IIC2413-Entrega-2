import csv
import psycopg2

def carga_cliente(archivo_csv, tabla, cursor):
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
                    SQL = f"INSERT INTO {tabla} (id, nombre, email, clave, fono) VALUES (%s, %s, %s, %s, %s)"
                    data = (id, cliente[0], cliente[1], cliente[2], cliente[3],)
                    cursor.execute(SQL, data)
                    id += 1
                except psycopg2.IntegrityError as error:
                    print(f"Error de integridad: {error}")
                    conn.rollback()  # Rollback para evitar transacciones inconsistentes
                else:
                    conn.commit()  # Commit para guardar los cambios
                    print("Una carga lista")
            else:
                print(f"Cliente {cliente[1]} ya existe")

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
            archivo_csv = 'clientes.csv'
            nombre_tabla = 'Clientes'
            carga_cliente(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")





