from django.shortcuts import render
from django.db.models import Q, Sum
import psycopg2
from .models import Clientes, Platos, Restaurantes, Pedidos, PedidosPlatos, Deliverys, PlatosRestaurantes, Calificaciones, Suscripciones
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_USER_PASSWORD = os.getenv('DATABASE_USER_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')


def index(request):
    clientes = Clientes.objects.all()
    return render(request, 'index.html', {'clientes':clientes})

def consulta_1(request):
    if request.method == 'POST':
        consulta = request.POST.get('consulta', '')
        platos = Platos.objects.filter(nombre__icontains = consulta)
        restaurantes = Restaurantes.objects.filter(platosrestaurantes__id_plato__in=platos, vigencia = True).distinct()
        context = {
            'restaurantes': restaurantes,
            'consulta': consulta
        }
        return render(request, 'consulta_1.html', context)
    else:
        return render(request, 'consulta_1.html')
    
def consulta_2(request):
    if request.method == 'POST':
        email = request.POST.get('email','')
        cliente = Clientes.objects.filter(email=email).first()
        if cliente:
            pedidos = Pedidos.objects.filter(id_cliente=cliente)
            context = {
                'pedidos': pedidos,
                'cliente': cliente,
            }
            return render(request, 'consulta_2.html', context)
        else:
            error_message = "Cliente no encontrado"
            return render(request, 'consulta_2.html', {'error_message': error_message})
    else:
        return render(request, 'consulta_2.html')
    
def calcular_precio_total_pedido(pedido):
    pedidos_platos = PedidosPlatos.objects.filter(id_pedido=pedido)
    print("Platos asociados al pedido:", pedidos_platos)
    precio_total = sum(pedido_plato.id_plato.precio for pedido_plato in pedidos_platos)
    print("Precio total calculado:", precio_total)
    return precio_total
    
def consulta_3(request):
    pedidos_concretados = Pedidos.objects.filter(estado='entregado a cliente')
    pedidos_cancelados = Pedidos.objects.filter(
        Q(estado='Cliente cancela ') |
        Q(estado='restaurant cancela') |
        Q(estado='delivery cancela ')
    )

    for pedido in pedidos_concretados:
        pedido.precio_total = calcular_precio_total_pedido(pedido)
    for pedido in pedidos_cancelados:
        pedido.precio_total = calcular_precio_total_pedido(pedido)

    context = {
        'pedidos_concretados': pedidos_concretados,
        'pedidos_cancelados': pedidos_cancelados,
    }
    return render(request, 'consulta_3.html', context)

def consulta_4(request):
    if request.method == 'POST':
        estilo_plato = request.POST.get('estilo_plato', None)
        if estilo_plato:
            platos = Platos.objects.filter(estilo=estilo_plato)
            print(platos)
            platos_restaurantes = PlatosRestaurantes.objects.filter(id_plato__in=platos)
            restaurantes = Restaurantes.objects.filter(id__in=platos_restaurantes.values('id_restaurante'))
            deliverys = Deliverys.objects.filter(id__in=restaurantes.values('id'))
            return render(request, 'consulta_4.html', {'platos': platos, 'restaurantes': restaurantes, 'deliverys': deliverys, 'estilo_plato': estilo_plato})
    return render(request, 'consulta_4.html')

def consulta_5(request):
    estilo_plato = request.GET.get('estilo_plato')
    if estilo_plato:
        platos = Platos.objects.filter(estilo=estilo_plato)
        return render(request, 'consulta_5.html', {'platos': platos, 'estilo_plato': estilo_plato})
    return render(request, 'consulta_5.html')

def consulta_6(request):
    cliente_email = request.GET.get('cliente_email')
    if cliente_email:
        try:
            cliente = Clientes.objects.get(email=cliente_email)
            suscripciones = Suscripciones.objects.filter(id_cliente=cliente)
            restaurantes = []
            for suscripcion in suscripciones:
                restaurante = suscripcion.id_delivery.nombre
                restaurantes.append(restaurante)
            return render(request, 'consulta_6.html', {'cliente_email': cliente_email, 'restaurantes': restaurantes})
        except Clientes.DoesNotExist:
            error_message = "Cliente no encontrado."
            return render(request, 'consulta_6.html', {'error_message': error_message})
    return render(request, 'consulta_6.html')

def consulta_7(request):
    clientes = Clientes.objects.all()
    total_gastado_por_cliente = {}
    for cliente in clientes:
        pedidos_no_suscripcion = Pedidos.objects.filter(id_cliente=cliente).exclude(id__in=Suscripciones.objects.filter(id_cliente=cliente).values('id_delivery'))
        total_gastado = pedidos_no_suscripcion.aggregate(Sum('id_delivery__precio_mensual'))['id_delivery__precio_mensual__sum']
        total_gastado_por_cliente[cliente] = total_gastado if total_gastado else 0
    return render(request, 'consulta_7.html', {'total_gastado_por_cliente': total_gastado_por_cliente})

def consulta_8(request):
    platos = Platos.objects.all()
    platos_con_restaurantes = []
    for plato in platos:
        restaurantes = PlatosRestaurantes.objects.filter(id_plato=plato)
        platos_con_restaurantes.append({'plato': plato, 'restaurantes': restaurantes})
    return render(request, 'consulta_8.html', {'platos_con_restaurantes': platos_con_restaurantes})

def consulta_9(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        if numero and 1 <= int(numero) <= 5:
            evaluaciones = Calificaciones.objects.filter(cal_cliente__gte=numero, cal_despachador__gte=numero)
            return render(request, 'consulta_9.html', {'evaluaciones': evaluaciones, 'numero': numero})
        else:
            error_message = "El número debe estar entre 1 y 5"
            return render(request, 'consulta_9.html', {'error_message': error_message})
    else:
        return render(request, 'consulta_9.html')
    
def consulta_10(request):
    if request.method == 'POST':
        alergeno = request.POST.get('alergeno')
        if alergeno:
            platos_con_alergeno = Platos.objects.filter(ingredientes__icontains=alergeno)
            return render(request, 'consulta_10.html', {'platos_con_alergeno': platos_con_alergeno, 'alergeno': alergeno})
        else:
            error_message = "Debe ingresar un alérgeno"
            return render(request, 'consulta_10.html', {'error_message': error_message})
    else:
        return render(request, 'consulta_10.html')
    
def consulta_general(request):
    if request.method == 'POST':
        atributos = request.POST.get('atributos')
        tablas = request.POST.get('tablas')
        condiciones = request.POST.get('condiciones')

        if atributos and tablas:
            if isinstance(atributos, str) and isinstance(tablas, str):
                conn = psycopg2.connect(
                    host= DATABASE_HOST,
                    user=DATABASE_USER,
                    password=DATABASE_USER_PASSWORD,
                    port=DATABASE_PORT,
                    database=DATABASE_NAME
                )

                cursor = conn.cursor()
                if condiciones:
                    cursor.execute("SELECT {} FROM {} WHERE {}".format(atributos, tablas, condiciones))
                else:
                    cursor.execute("SELECT {} FROM {}".format(atributos, tablas))
                    
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]

                cursor.close()
                conn.close()

                return render(request, 'consulta_general.html', {'results': results, 'column_names': column_names})
            else:
                error_message = "Los atributos y las tablas deben ser strings válidos."
                return render(request, 'consulta_general.html', {'error_message': error_message})
        else:
            error_message = "Atributos y tablas son campos obligatorios."
            return render(request, 'consulta_general.html', {'error_message': error_message})
    else:
        return render(request, 'consulta_general.html')
