from django.shortcuts import render
from django.http import HttpResponse

# Importamos los repositorios y casos de uso
from infrastructure.mongo_repositories import MongoCatalogoRepository, MongoPedidoRepository
from use_cases.catalogo_use_cases import ConsultarCatalogoUseCase
from use_cases.pedidos_use_cases import CrearPedidoUseCase
from datetime import datetime

def index(request):
    """Renderiza la Landing Page Premium con Tailwind CSS"""
    return render(request, 'index.html')

def platos_list(request):
    """Devuelve la lista parcial via HTMX con el catálogo de platos"""
    # Inyección de dependencias manual (en producción se puede usar dependency-injector)
    catalogo_repo = MongoCatalogoRepository()
    use_case = ConsultarCatalogoUseCase(catalogo_repo)
    platos = use_case.execute()
    
    # Solo devolvemos la porcion para HTMX
    return render(request, 'partials/plato_list.html', {'platos': platos})

def crear_pedido(request):
    """Ejemplo simplificado de caso de uso para procesar un POST."""
    if request.method == 'POST':
        # Instanciar el caso de uso con su repositorio correspondiente
        repo = MongoPedidoRepository()
        use_case = CrearPedidoUseCase(repo)
        
        # Parseo simple o simulación. Lo ideal sería coger los ids del body request.
        id_cliente = "cliente_invitado" 
        direccion = request.POST.get('direccion', 'A mesa 3')
        platos_ids = request.POST.getlist('platos')
        
        nuevo_id = use_case.execute(id_cliente, direccion, platos_ids, datetime.now())
        return HttpResponse(f"<span class='text-green-400 font-bold'>¡Pedido #{nuevo_id[:8]} creado! En preparación.</span>")
    return HttpResponse("Método no permitido", status=405)
