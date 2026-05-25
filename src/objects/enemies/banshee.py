from src.objects.enemies import Enemy


class Banshee(Enemy):
    """Баньши - мощный босс-подобный враг"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'banshee')

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': 48,
            'height': 48,
            'speed': 90,  # Очень медленный
            'health': 200,  # Очень много здоровья
            'damage': 25,  # Огромный урон
            'attack_range': 50  # Ближний бой
        }

    def get_color(self) -> tuple:
        return (75, 0, 130)  # Тёмно-фиолетовый