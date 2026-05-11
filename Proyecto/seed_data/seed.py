import requests
import os

API_URL = "http://localhost:5000/api/dishes/"

dishes = [
    {
        "nombre_plato": "Samosas de Verdura",
        "descripcion": "Empanadillas crujientes rellenas de patata especiada y guisantes, acompañadas de chutney de menta.",
        "precio_plato": 4.50,
        "categoria": "ENTRANTE",
        "visibilidad": "AMBOS",
        "file_name": "samosas_verdura.png"
    },
    {
        "nombre_plato": "Momos de Pollo",
        "descripcion": "Dumplings tradicionales al vapor rellenos de pollo picado y especias del Himalaya.",
        "precio_plato": 6.50,
        "categoria": "ENTRANTE",
        "visibilidad": "AMBOS",
        "file_name": "momos_pollo.png"
    },
    {
        "nombre_plato": "Pollo Tikka Masala",
        "descripcion": "Tiernos trozos de pollo asado marinados en yogur, bañados en una cremosa salsa de tomate y curry.",
        "precio_plato": 12.90,
        "categoria": "PRINCIPAL",
        "visibilidad": "AMBOS",
        "file_name": "tikka_masala.png"
    },
    {
        "nombre_plato": "Cordero Rogan Josh",
        "descripcion": "Cordero cocinado a fuego lento en una aromática y espesa salsa roja de Cachemira.",
        "precio_plato": 14.50,
        "categoria": "PRINCIPAL",
        "visibilidad": "DIARIO",
        "file_name": "rogan_josh.png"
    },
    {
        "nombre_plato": "Gulab Jamun",
        "descripcion": "Bolas de leche frita empapadas en un fragante almíbar de cardamomo y agua de rosas.",
        "precio_plato": 5.00,
        "categoria": "POSTRE",
        "visibilidad": "AMBOS",
        "file_name": "gulab_jamun.png"
    },
    {
        "nombre_plato": "Mango Lassi",
        "descripcion": "Refrescante batido tradicional a base de yogur espeso y pulpa de mango fresco.",
        "precio_plato": 4.00,
        "categoria": "POSTRE",
        "visibilidad": "AMBOS",
        "file_name": "mango_lassi.png"
    },
    {
        "nombre_plato": "Naan de Ajo y Queso",
        "descripcion": "Pan plano horneado en horno tandoor con un toque de ajo y queso derretido.",
        "precio_plato": 3.50,
        "categoria": "ENTRANTE",
        "visibilidad": "AMBOS",
        "file_name": "naan_ajo_queso.png"
    },
    {
        "nombre_plato": "Pakoras de Cebolla",
        "descripcion": "Tiras de cebolla rebozadas en harina de garbanzo con especias indias y fritas hasta quedar crujientes.",
        "precio_plato": 4.00,
        "categoria": "ENTRANTE",
        "visibilidad": "DIARIO",
        "file_name": "pakoras_cebolla.png"
    },
    {
        "nombre_plato": "Arroz Pilaf con Especias",
        "descripcion": "Arroz basmati aromático cocinado con azafrán, cardamomo, clavo y canela.",
        "precio_plato": 4.50,
        "categoria": "PRINCIPAL",
        "visibilidad": "CARTA",
        "file_name": "arroz_pilaf.png"
    },
    {
        "nombre_plato": "Pollo Korma",
        "descripcion": "Suave y aromático pollo cocinado en una salsa cremosa de anacardos y coco.",
        "precio_plato": 13.50,
        "categoria": "PRINCIPAL",
        "visibilidad": "AMBOS",
        "file_name": "pollo_korma.png"
    },
    {
        "nombre_plato": "Helado Kulfi de Pistacho",
        "descripcion": "El helado tradicional indio, denso y cremoso, con trozos de pistacho y un toque de azafrán.",
        "precio_plato": 5.50,
        "categoria": "POSTRE",
        "visibilidad": "DIARIO",
        "file_name": "kulfi_pistacho.png"
    }
]

def seed_database():
    print("🌶️ Iniciando la inyección de platos del Himalaya...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for dish in dishes:
        img_path = os.path.join(script_dir, dish["file_name"])
        
        data = {
            "nombre_plato": dish["nombre_plato"],
            "descripcion": dish["descripcion"],
            "precio_plato": dish["precio_plato"],
            "categoria": dish["categoria"],
            "visibilidad": dish["visibilidad"]
        }
        
        try:
            if dish["file_name"] != "":
                with open(img_path, 'rb') as f:
                    files = {'imagen': (dish["file_name"], f, 'image/png')}
                    response = requests.post(API_URL, data=data, files=files)
            else:
                response = requests.post(API_URL, data=data)
                
            if response.status_code in [200, 201]:
                print(f"✅ Subido con éxito: {dish['nombre_plato']}")
            else:
                print(f"❌ Error al subir {dish['nombre_plato']}: {response.text}")
                
        except FileNotFoundError:
            print(f"⚠️ Imagen no encontrada para {dish['nombre_plato']} en {img_path}")
        except Exception as e:
            print(f"🔥 Fallo de red con la API: {e}")

if __name__ == "__main__":
    seed_database()
