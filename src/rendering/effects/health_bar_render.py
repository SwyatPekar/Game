import pygame
from src.core import config


class HealthBarRenderer:
    @staticmethod
    def render(screen: pygame.Surface, entity, is_enemy: bool = False):
        if is_enemy:
            bar_width = entity.width
            bar_height = config.health_bar_height_enemy
            offset_y = config.health_bar_offset_y_enemy
        else:
            bar_width = config.health_bar_width
            bar_height = config.health_bar_height
            offset_y = config.health_bar_offset_y

        bar_x = entity.x - (bar_width - entity.width) / 2
        bar_y = entity.y - offset_y

        pygame.draw.rect(screen, config.red, (bar_x, bar_y, bar_width, bar_height))

        health_width = int(bar_width * (entity.health / entity.max_health))
        pygame.draw.rect(screen, config.green, (bar_x, bar_y, health_width, bar_height))

        pygame.draw.rect(screen, config.black, (bar_x, bar_y, bar_width, bar_height), 1)