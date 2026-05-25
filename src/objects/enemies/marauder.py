from src.objects.enemies import Enemy


class Marauder(Enemy):
    """Налётчик - средний враг с дальнобойной атакой"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 'marauder')
        self.attack_range = 250  # Дальнобойный

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': 32,
            'height': 32,
            'speed': 130,
            'health': 60,
            'damage': 12,
            'attack_range': 250  # Стреляет издалека
        }

    def get_color(self) -> tuple:
        return (255, 140, 0)  # Оранжевый