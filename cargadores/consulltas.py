import psycopg2
#1 Dado un plato -> Restaunrantes
def Restaurantes_por_Plato(plato_id, cur):
 
    SQL = '''
    SELECT R.id, R.nombre, PR.vigencia
    FROM Plato_Restaurante PR
    JOIN Restaurante R ON PR.id_restaurante = R.id
    WHERE PR.id_plato = %s;
    '''
    valores = (plato_id,)

    try:
        cur.execute(SQL,valores)
        resultados = cur.fetchall()
        return resultados
    except Exception as error:
        print("Error:", error)
        return None

#2 Dado un usuario -> Pedido - Gasto (concretdo)
def pedido_usuario(email, cur):

    SQL ='''
    SELECT pe.id, SUM(pl.precio)
    FROM pedidos pe
    JOIN pedidos_plato pepl ON pe.id = pepl.id_pedido
    JOIN plato pl ON pepl.id_plato = pl.id
    WHERE pedidos.id_cliente = %s
    GROUP BY pe.id;
'''
    try:
        cur.execute(
            "SELECT id FROM clientes WHERE clientes.email = %s",(email,)
        )
        cliente = cur.fetchone()
        if cliente:
            valor = (cliente[0],)
            cur.execute(SQL,valor)
            respuesta = cur.fetchall()
            if respuesta:
                return respuesta
            else:
                return "Usuario sin pedidos"
        else:
            return "Usuario no Encontrado"
    except Exception as error:
        print("ERROR:", error)
        pass

#3 Dado nada -> Todos los pedidos - Valor 
def pedidos_total(cur):

    try:
        SQL = '''
        SELECT pe.id, pe.estado ,SUM(pl.precio)
        FROM pedidos pe
        JOIN pedidos_plato pepl ON pe.id = pepl.id_pedido
        JOIN plato pl ON pepl.id_plato = pl.id
        GROUP BY pe.id;
        '''
        cur.execute(SQL)
        datos = cur.fetchall()
        return datos
    except Exception as error:
        print("Ocurrio un error:", error)

    pass

#4 Dado un Estilo -> platos - restauntates - opcion delivey
def estilo_plato(Estilo,cur):
    SQL = '''
    SELECT pl.nombre, re.nombre
    FROM platos pl
    JOIN plato_restaurantes plre ON pl.id = plre.id_plato
    JOIN restaurantes re ON re.id = plre.id_restaurante
    WHERE pl.estilo = %s;
    '''
    try: 
        a = 1
    except Exception as error:
        print("Ocurrio un error:",error)

    pass


#5 Dado un Estilo -> paltos - restriccion
def estilo_plato_2():
    pass

#6 Dado un Cliente (email) -> acceso a suscripciones
def suscripcion_usuairo():
    pass

#7 Dado Nada -> todos cliente - Dinero Gastado
def gasto_clientes():
    pass

#8 Dado NADA -> todos los platos - restaurante
def plato_restaurantes():
    pass

#9 Dado numero -> Calificaciones superior o igual
def evaluaciones_sup():
    pass

#10 Dado un alergeno -> platos que lo tienen como ingrediente
def alergeno_plato():
    pass

    