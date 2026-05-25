import pygame
import math
from abc import ABC, abstractmethod


class Entity(ABC):
    """Базовый класс для всех игровых объектов (Model)"""

    def __init__(self, x: float, y: float, width: int, height: int, speed: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = 100
        self.max_health = 100
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0

    @abstractmethod
    def update(self, dt: float):
        """Обновление состояния объекта"""
        pass

    def draw(self, screen: pygame.Surface, renderer=None):
        """
        Отрисовка объекта (делегирование рендереру)

        Args:
            screen: Поверхность для отрисовки
            renderer: Опциональный рендерер для кастомной отрисовки
        """
        if renderer:
            renderer.render(screen, self)

    def get_rect(self) -> pygame.Rect:
        """Получить прямоугольник объекта для коллизий"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage: int):
        """Получение урона"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        """Смерть объекта"""
        self.is_alive = False

    def check_collision(self, other: 'Entity') -> bool:
        """Проверка столкновения с другим объектом (AABB)"""
        return self.get_rect().colliderect(other.get_rect())

    def distance_to(self, other: 'Entity') -> float:
        """Вычисление расстояния до другого объекта"""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

