from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluimos las rutas de nuestra aplicación web (capa de adaptadores / delivery)
    path('', include('delivery.urls')),
]
