import pygame
from src.rendering.render import BaseRenderer


class EntityRenderer(BaseRenderer):
    def render(self, screen: pygame.Surface, entity):
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        pygame.draw.rect(screen, entity.get_color() if hasattr(entity, 'get_color') else (255, 255, 255), rect)