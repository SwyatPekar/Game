from src.objects.enemies.enemy import Enemy


class Cannibal(Enemy):
    """Каннибал - медленный, сильный враг"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'cannibal')

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': 36,
            'height': 36,
            'speed': 100,  # Медленный
            'health': 80,  # Много здоровья
            'damage': 15,  # Сильный урон
            'attack_range': 40  # Ближний бой
        }

    def get_color(self) -> tuple:
        return (128, 0, 128)  # Фиолетовый