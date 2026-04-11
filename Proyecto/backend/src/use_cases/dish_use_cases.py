import uuid
from src.domain.models import Dish

class ManageDishesUseCase:
    def __init__(self, dish_repo):
        self.dish_repo = dish_repo

    def create_dish(self, data: dict) -> Dish:
        dish_id = str(uuid.uuid4())
        new_dish = Dish(id=dish_id, **data)
        self.dish_repo.save(new_dish)
        return new_dish

    def list_dishes(self):
        return self.dish_repo.get_all()

    def remove_dish(self, dish_id: str):
        self.dish_repo.delete(dish_id)