import csv
import psycopg2

def carga_pedidos_platos(archivo_csv, tabla, cursor):
    with open(archivo_csv, 'r') as f:
        datos = csv.reader(f)
        next(datos)
        for dato in datos:
            platos_ids = datos[4].split()
            for id in platos_ids:
                cursor.execute(
                    "SELECT id FROM Platos WHERE id = %s",
                    (id,)
                )
                row = cursor.fetchone()
                if row:
                    try:
                        SQL = f"INSERT INTO {tabla} (id_pedido, id_plato) VALUES (%s, %s)",
                        data = (dato[0], id,)
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
            archivo_csv = 'pedidos2.csv'
            nombre_tabla = 'Pedidos_platos'
            carga_pedidos_platos(archivo_csv, nombre_tabla, cur)
            print("Carga Finalizada")
except Exception as Error:
    print(f"No se pudo conectar: {Error}")