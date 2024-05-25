import csv
import psycopg2

def carga_direcciones(archivo_csv, tabla, cursor):
    id = 1  # para los id
    with open(archivo_csv, 'r') as f:
        Direcciones = csv.reader(f)
        next(Direcciones)  # me salto la primera fila (cabecera)
        for direccion in Direcciones:
            cursor.execute(
                '''SELECT id FROM Clientes
                WHERE Clientes.email = %s''',
                (direccion[1],)
            )
            cliente = cursor.fetchone()
            if cliente:            
                try:
                    SQL = f"INSERT INTO {tabla} (id, id_cliente, dirrecion, cut_comuna) VALUES (%s, %s, %s, %s)"
                    data = (id,cliente[0] , direccion[4], direccion[5],)
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
            archivo_csv = 'clientes.csv'
            nombre_tabla = 'Direcciones'
            carga_direcciones(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")
