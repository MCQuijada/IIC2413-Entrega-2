def carga_delivery(tabla_csv, tabla, cursor):
    id = 1 #para los id
    datos = tabla_csv.reader(tabla_csv)
    next(datos) #me salto lo primero
    for dato in datos:
        if True:
            try:
                cursor.executable(
                    f"INSERT INTO {tabla} VALUES (id, nombre, vigencia, fono, tiempo_despacho, precio_unitario, precio_mensual, precio_anual)" ,
                    (id, dato[4],dato[5],dato[6],dato[7],dato[8], dato[9], dato[10],)
                )
                id +=1
            except psycopg2.IntegrityError as Error:
                print(f"Error de integridad: {Error}")


cur = conn.cursor()
archivo_csv = 'cldeldes.csv'
nombre_tabla = 'Sucursales'
carga_tabla(archivo_csv, nombre_tabla, cur)
conn.commit()
cur.close()
conn.close()