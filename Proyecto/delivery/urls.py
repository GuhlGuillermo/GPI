from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('platos/', views.platos_list, name='platos_list'),
    path('pedido/crear/', views.crear_pedido, name='crear_pedido'),
]
