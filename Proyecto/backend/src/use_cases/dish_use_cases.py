import uuid
from typing import List, Dict, Any
from src.domain.models import Dish
from src.infrastructure.database.mongo_repos import MongoDishRepository

class DishUseCases:
    def __init__(self, dish_repo: MongoDishRepository):
        self.dish_repo = dish_repo

    def get_all_dishes(self, active_only: bool = True) -> List[Dish]:
        return self.dish_repo.get_all(active_only=active_only)
        
    def get_dish(self, dish_id: str) -> Dish:
        dish = self.dish_repo.get_by_id(dish_id)
        if not dish:
            raise ValueError(f"Dish with id {dish_id} not found")
        return dish

    def create_dish(self, nombre_plato: str, descripcion: str, precio_plato: float, categoria: str, url_imagen: str = "") -> Dish:
        dish = Dish(
            id_plato=str(uuid.uuid4()),
            nombre_plato=nombre_plato,
            descripcion=descripcion,
            precio_plato=precio_plato,
            categoria=categoria,
            url_imagen=url_imagen,
            activo=True,
            es_de_temporada=False
        )
        self.dish_repo.save(dish)
        return dish

    def update_dish(self, dish_id: str, updates: Dict[str, Any]) -> Dish:
        dish = self.get_dish(dish_id)
        
        if 'nombre_plato' in updates: dish.nombre_plato = updates['nombre_plato']
        if 'descripcion' in updates: dish.descripcion = updates['descripcion']
        if 'precio_plato' in updates: dish.precio_plato = updates['precio_plato']
        if 'categoria' in updates: dish.categoria = updates['categoria']
        if 'url_imagen' in updates: dish.url_imagen = updates['url_imagen']
        if 'es_de_temporada' in updates: dish.es_de_temporada = updates['es_de_temporada']
        if 'activo' in updates: dish.activo = updates['activo']
        
        self.dish_repo.save(dish)
        return dish

    def delete_dish(self, dish_id: str) -> None:
        """Borrado lógico del plato"""
        dish = self.get_dish(dish_id)
        dish.activo = False
        self.dish_repo.save(dish)
