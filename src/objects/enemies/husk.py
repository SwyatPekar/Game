from src.objects.enemies import Enemy
from src.core.config import blue
from typing import Dict, Any


class Husk(Enemy):
    """Враг типа Husk - быстрый, но слабый."""

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'husk')

    @staticmethod
    def get_enemy_stats(enemy_type: str) -> Dict[str, Any]:
        """Возвращает характеристики Husk."""
        return {
            'width': 28,
            'height': 28,
            'speed': 180,
            'health': 30,
            'damage': 8,
            'attack_range': 35
        }

    def get_color(self) -> tuple:
        return blue