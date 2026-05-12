import requests
import json
import time

API_URL = "http://localhost:5000/api/orders/"

def test_ram_order():
    print("🚀 Iniciando prueba de inserción de pedido directo a RAM...")

    payload = {
        "id_usuario": "invitado",
        "nombre": "Tester RAM",
        "email": "test.ram@saborgpi.local",
        "credit_card": "1234567812345678", # 16 dígitos válidos
        "dir_entrega": "Calle de la Memoria Virtual 123",
        "ignore_schedule": True, # Forzamos el bypass de las horas
        "items": [
            {
                "id_plato": "plato_test_1",
                "nombre_plato": "Pollo Tikka Masala Virtual",
                "precio_plato": 12.90,
                "cantidad": 2
            },
            {
                "id_plato": "plato_test_2",
                "nombre_plato": "Naan de Pruebas",
                "precio_plato": 3.50,
                "cantidad": 1
            }
        ]
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ ¡Pedido Creado con Éxito!")
            print(f"ID del Pedido: {data['id_pedido']}")
            print(f"Estado: {data['estado']}")
            print(f"Importe Total: {data['importe_total']}€")
            print("\n👀 Ahora deberías ver este pedido en el Dashboard, en tiempo real, pero si revisas MongoDB, ¡NO estará ahí hasta que hagas click en 'Ejecutar Cierre de Caja'!")
        else:
            print(f"❌ Error al crear el pedido: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"🔥 Fallo de red: {e}")

if __name__ == "__main__":
    test_ram_order()
