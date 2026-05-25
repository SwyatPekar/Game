"""
Базовые классы для системы рендеринга.
"""
import pygame
from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """Абстрактный базовый класс для всех рендереров"""

    @abstractmethod
    def render(self, screen: pygame.Surface, entity):
        """
        Отрисовка сущности

        Args:
            screen: Поверхность для отрисовки
            entity: Сущность для отрисовки
        """
        pass