"""
Базовый рендерер для всех игровых объектов.
"""
import pygame
from src.rendering.render import BaseRenderer


class EntityRenderer(BaseRenderer):
    """Базовый класс для отрисовки сущностей"""

    def render(self, screen: pygame.Surface, entity):
        """
        Отрисовка базовой сущности (прямоугольник)

        Args:
            screen: Поверхность для отрисовки
            entity: Сущность для отрисовки
        """
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        pygame.draw.rect(screen, entity.get_color() if hasattr(entity, 'get_color') else (255, 255, 255), rect)