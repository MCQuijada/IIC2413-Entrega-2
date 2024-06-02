from django.http import HttpResponse

from .models import Clientes

def index(request):
    clientes = Clientes.objects.all()
    return HttpResponse(request, 'index.html', {'clientes':clientes})


