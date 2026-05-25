from src.objects.enemies import Enemy
from src.core.config import blue


class Husk(Enemy):
    """Хаск - быстрый, слабый враг ближнего боя"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'husk')

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': 28,
            'height': 28,
            'speed': 180,  # Быстрый
            'health': 30,  # Мало здоровья
            'damage': 8,  # Слабый урон
            'attack_range': 35  # Ближний бой
        }

    def get_color(self) -> tuple:
        return blue