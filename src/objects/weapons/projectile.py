import math
import pygame


class Projectile:
    """
    Model: Базовый класс для всех снарядов (пули, гранаты).
    Содержит только данные и логику движения.
    НЕ содержит отрисовку (это задача RenderSystem).
    """

    def __init__(self, x: float, y: float, angle: float, speed: float, damage: int, owner_type: str):
        """
        :param x: Начальная позиция X
        :param y: Начальная позиция Y
        :param angle: Угол полета в радианах
        :param speed: Скорость полета (пикселей в секунду)
        :param damage: Урон при попадании
        :param owner_type: Кто стрелял ('player' или 'enemy'), для фильтрации коллизий
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.owner_type = owner_type

        # Физические параметры
        self.radius = 4  # Радиус для коллизии
        self.is_active = True  # Флаг активности (если False - удалить)

    def update(self, dt: float):
        """Обновление позиции снаряда за кадр"""
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt

    @property
    def rect(self) -> pygame.Rect:
        """
        Возвращает хитбокс (AABB) для проверки столкновений.
        Используем квадрат вокруг центра для упрощения расчетов на этапе MVP.
        """
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )