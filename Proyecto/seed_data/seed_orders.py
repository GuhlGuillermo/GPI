import os
import sys
import random
from unittest.mock import patch
import datetime

# Asegurarnos de que Python puede encontrar el módulo 'src' y 'app'
# subiendo un nivel desde seed_data a Proyecto/backend
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_path)

from app import create_app

# Lista de clientes ficticios
CLIENTES = [
    {"nombre": "Laura Sánchez", "email": "laura@ejemplo.com", "dir": "Calle del Pez 4, 2B"},
    {"nombre": "Carlos Gómez", "email": "carlos@ejemplo.com", "dir": "Gran Vía 12, 5D"},
    {"nombre": "María Rodríguez", "email": "maria@ejemplo.com", "dir": "Av. Libertad 34"},
    {"nombre": "David Fernández", "email": "david@ejemplo.com", "dir": "Calle Luna 9, Bajo"},
    {"nombre": "Elena López", "email": "elena@ejemplo.com", "dir": "Plaza Mayor 1, 1A"},
    {"nombre": "Javier Martín", "email": "javier@ejemplo.com", "dir": "Calle Sol 22"},
    {"nombre": "Carmen Pérez", "email": "carmen@ejemplo.com", "dir": "Paseo del Prado 45"},
    {"nombre": "Alejandro Ruiz", "email": "alejandro@ejemplo.com", "dir": "Ronda Sur 88"},
]

def generate_random_card():
    # Tarjeta ficticia de 16 dígitos
    return "4" + "".join([str(random.randint(0, 9)) for _ in range(15)])

def main():
    print("🤖 Iniciando Simulador de Tráfico de Clientes (Modo Flask TestClient)")
    print("⏳ Congelando el tiempo a las 14:00h de un Lunes para evitar bloqueos...")

    # Creamos la aplicación y el cliente de pruebas
    app = create_app()
    client = app.test_client()

    # Hacemos una petición para obtener los platos disponibles
    response = client.get('/api/dishes/')
    if response.status_code != 200:
        print(f"❌ Error al obtener los platos: {response.status_code}")
        return

    todos_los_platos = response.get_json()
    if not todos_los_platos:
        print("❌ La carta está vacía. Ejecuta seed.py primero.")
        return

    # Mockeamos el datetime dentro de order_use_cases.py para saltarnos las validaciones
    mock_date = datetime.datetime(2026, 4, 13, 14, 0, 0) # Lunes a las 14:00

    # Realizamos 15 pedidos aleatorios
    with patch('src.use_cases.order_use_cases.datetime') as mock_datetime:
        mock_datetime.now.return_value = mock_date

        for i in range(1, 16):
            cliente = random.choice(CLIENTES)
            
            # Seleccionamos entre 2 y 4 platos aleatorios
            num_items = random.randint(2, 4)
            platos_seleccionados = random.sample(todos_los_platos, num_items)
            
            items_pedido = []
            subtotal = 0.0
            
            for plato in platos_seleccionados:
                cantidad = random.randint(1, 2)
                subtotal += plato["precio_plato"] * cantidad
                items_pedido.append({
                    "id_plato": plato["id_plato"],
                    "nombre_plato": plato["nombre_plato"],
                    "precio_plato": plato["precio_plato"],
                    "cantidad": cantidad
                })
            
            # Asegurar que el pedido supera los 15€ si no lo hace, añadimos más cantidad al primero
            if subtotal < 15.0:
                falta = 15.0 - subtotal
                plato_caro = max(items_pedido, key=lambda x: x["precio_plato"])
                cantidad_extra = int((falta // plato_caro["precio_plato"]) + 1)
                plato_caro["cantidad"] += cantidad_extra

            payload = {
                "id_usuario": "invitado",
                "items": items_pedido,
                "credit_card": generate_random_card(),
                "nombre": cliente["nombre"],
                "email": cliente["email"],
                "dir_entrega": cliente["dir"]
            }

            res = client.post('/api/orders/', json=payload)
            
            if res.status_code == 201:
                order_data = res.get_json()
                print(f"✅ Pedido #{i:02d}: {cliente['nombre']} gastó {order_data['importe_total']:.2f}€ ({len(items_pedido)} platos distintos)")
            else:
                print(f"❌ Error en Pedido #{i}: {res.get_json()}")

        # Volcamos la memoria RAM simulada a MongoDB para que el servidor principal pueda leerla
        from src.use_cases.billing_buffer import BillingBufferManager
        print("\n💾 Volcando la memoria simulada a MongoDB...")
        with app.app_context():
            BillingBufferManager().flush_to_db()

    print("\n🎉 Simulación completada con éxito.")
    print("📈 Ve a http://localhost:5173/chef-admin/facturacion y haz clic en 'Refrescar Datos'. ¡Los números saltarán a la vista!")

if __name__ == "__main__":
    main()
