from src.objects.enemies.enemy import Enemy
from src.core.config import blue


class Husk(Enemy):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'husk')

    def get_enemy_stats(self, enemy_type: str) -> dict:
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