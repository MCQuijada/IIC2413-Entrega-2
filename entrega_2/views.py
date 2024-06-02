from django.shortcuts import render

from .models import Clientes, Platos, Restaurantes, Pedidos

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
    
