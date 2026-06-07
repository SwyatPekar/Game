import pygame
import math
from src.core import config


class PlayerRenderer:
    @staticmethod
    def render(screen: pygame.Surface, player):
        surface = pygame.Surface((player.width, player.height), pygame.SRCALPHA)

        color = (100, 100, 255, 180) if player.invincible else (*config.green, 255)
        pygame.draw.rect(surface, color, (0, 0, player.width, player.height))

        rotated = pygame.transform.rotate(surface, -math.degrees(player.facing_angle))
        rect = rotated.get_rect(center=(player.x + player.width / 2, player.y + player.height / 2))
        screen.blit(rotated, rect)

        center_x = player.x + player.width / 2
        center_y = player.y + player.height / 2
        end_x = center_x + math.cos(player.facing_angle) * config.direction_line_length
        end_y = center_y + math.sin(player.facing_angle) * config.direction_line_length
        pygame.draw.line(screen, config.direction_line_color, (center_x, center_y), (end_x, end_y), 2)

        if config.debug_mode:
            if player.roll_cooldown > 0:
                font = pygame.font.SysFont("Arial", 12)
                text = font.render(f"Roll CD: {player.roll_cooldown:.1f}s", True, config.white)
                screen.blit(text, (player.x, player.y - 25))

            if config.show_collision_boxes:
                pygame.draw.rect(screen, config.red, player.get_rect(), 1)