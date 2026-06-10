import pygame
from src.core import config

class EntityRenderer():
    def render(self, screen: pygame.Surface, entity):
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        pygame.draw.rect(screen, entity.get_color() if hasattr(entity, 'get_color') else config.white, rect)