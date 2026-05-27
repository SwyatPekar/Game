import pygame
from src.core.config import health_bar_width, health_bar_height, health_bar_offset_y, black, red, green


class HealthBarRenderer:
    @staticmethod
    def render(screen: pygame.Surface, entity):
        bar_width = health_bar_width
        bar_height = health_bar_height
        bar_x = entity.x - (bar_width - entity.width) / 2
        bar_y = entity.y - health_bar_offset_y

        pygame.draw.rect(screen, red, (bar_x, bar_y, bar_width, bar_height))

        health_width = int(bar_width * (entity.health / entity.max_health))
        pygame.draw.rect(screen, green, (bar_x, bar_y, health_width, bar_height))

        pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height), 1)