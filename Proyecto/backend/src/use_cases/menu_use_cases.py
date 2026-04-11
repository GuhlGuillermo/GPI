from datetime import datetime
from src.domain.models import DailyMenuConfig

class ConfigureDailyMenuUseCase:
    def __init__(self, menu_repo):
        self.menu_repo = menu_repo

    def execute(self, config_data: dict):
        # El PDF exige 3 entrantes, 3 principales y 2 postres 
        config = DailyMenuConfig(**config_data)
        self.menu_repo.save(config)

class GetAvailableMenuUseCase:
    def __init__(self, menu_repo):
        self.menu_repo = menu_repo

    def execute(self, date_str: str):
        now = datetime.now()
        # Restricción: No disponible en fines de semana [cite: 26]
        is_weekend = now.weekday() >= 5
        # Restricción: Solo disponible de 13:00 a 16:00 [cite: 26]
        if is_weekend or not (13 <= now.hour < 16):
            return None
            
        return self.menu_repo.get_by_date(date_str)