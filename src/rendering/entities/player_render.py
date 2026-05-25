"""
Рендерер игрока.
"""
import pygame
import math
from src.core.config import (green, direction_line_color, direction_line_length, health_bar_width, health_bar_height,
                             health_bar_offset_y, black, red)


class PlayerRenderer:
    """
    Отвечает за отрисовку игрока.
    View-компонент, не содержит бизнес-логики.
    """

    @staticmethod
    def render(screen: pygame.Surface, player):
        """Отрисовка тела игрока"""
        surface = pygame.Surface((player.width, player.height), pygame.SRCALPHA)

        color = (100, 100, 255, 180) if player.invincible else (*green, 255)
        pygame.draw.rect(surface, color, (0, 0, player.width, player.height))

        # Поворот спрайта
        rotated = pygame.transform.rotate(surface, -math.degrees(player.facing_angle))
        rect = rotated.get_rect(center=(player.x + player.width / 2, player.y + player.height / 2))
        screen.blit(rotated, rect)

        # Рисуем индикатор направления прямо на экране (не обрезается вращением)
        center_x = player.x + player.width / 2
        center_y = player.y + player.height / 2
        end_x = center_x + math.cos(player.facing_angle) * direction_line_length
        end_y = center_y + math.sin(player.facing_angle) * direction_line_length
        pygame.draw.line(screen, direction_line_color, (center_x, center_y), (end_x, end_y), 2)

    @staticmethod
    def render_health_bar(screen: pygame.Surface, player):
        """
        Отрисовка полоски здоровья игрока

        Args:
            screen: Поверхность для отрисовки
            player: Объект игрока (Model)
        """
        bar_width = health_bar_width
        bar_height = health_bar_height
        bar_x = player.x - (bar_width - player.width) / 2
        bar_y = player.y - health_bar_offset_y

        # Фон полоски (красный)
        pygame.draw.rect(screen, red, (bar_x, bar_y, bar_width, bar_height))

        # Текущее здоровье (зеленое)
        health_width = int(bar_width * (player.health / player.max_health))
        pygame.draw.rect(screen, green, (bar_x, bar_y, health_width, bar_height))

        # Рамка
        pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height), 1)