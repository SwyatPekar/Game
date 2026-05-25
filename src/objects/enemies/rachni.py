from src.objects.enemies import Enemy


class Rachni(Enemy):
    """Рахни - быстрый насекомый враг"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'rachni')

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': 24,
            'height': 24,
            'speed': 200,  # Очень быстрый
            'health': 25,  # Очень мало здоровья
            'damage': 6,  # Слабый урон
            'attack_range': 30  # Ближний бой
        }

    def get_color(self) -> tuple:
        return (0, 100, 0)  # Тёмно-зелёный