import pytest
from src.domain.models import Dish
from src.use_cases.dish_use_cases import DishUseCases

class MockDishRepository:
    def __init__(self):
        self.storage = {}

    def save(self, dish: Dish):
        self.storage[dish.id_plato] = dish

    def get_by_id(self, dish_id: str) -> Dish:
        return self.storage.get(dish_id)

    def get_all(self, active_only: bool = True):
        dishes = list(self.storage.values())
        if active_only:
            return [d for d in dishes if d.activo]
        return dishes

def test_create_dish_visibility_default():
    repo = MockDishRepository()
    use_case = DishUseCases(repo)
    
    # Creamos un plato básico (sin visibilidad explícita)
    dish = use_case.create_dish("Pakora", "Buñuelo indio", 5.0, "ENTRANTE")
    
    assert dish.nombre_plato == "Pakora"
    assert dish.precio_plato == 5.0
    assert dish.activo is True
    # Debería usar el valor por defecto: AMBOS
    assert dish.visibilidad == "AMBOS"
    # Debe tener una imagen por defecto si no se le ha pasado
    assert dish.url_imagen == "/default-dish.png"

def test_delete_dish_logical_and_visibility():
    repo = MockDishRepository()
    use_case = DishUseCases(repo)
    
    dish = use_case.create_dish("Pakora", "Buñuelo indio", 5.0, "ENTRANTE")
    
    assert dish.activo is True
    
    # Borrado lógico
    use_case.delete_dish(dish.id_plato)
    
    deleted_dish = use_case.get_dish(dish.id_plato)
    assert deleted_dish.activo is False
    assert deleted_dish.visibilidad == "OCULTO"

def test_update_dish_visibility():
    repo = MockDishRepository()
    use_case = DishUseCases(repo)
    
    dish = use_case.create_dish("Momo", "Dumplings", 6.5, "ENTRANTE", visibilidad="DIARIO")
    assert dish.visibilidad == "DIARIO"
    
    use_case.update_dish(dish.id_plato, {"visibilidad": "CARTA", "precio_plato": 7.0})
    
    updated = use_case.get_dish(dish.id_plato)
    assert updated.visibilidad == "CARTA"
    assert updated.precio_plato == 7.0
