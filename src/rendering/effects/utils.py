import pygame
import math


def rotate_surface(surface: pygame.Surface, angle: float) -> pygame.Surface:
    return pygame.transform.rotate(surface, -angle)


def draw_direction_line(screen: pygame.Surface, center: tuple, angle: float,
                        length: int = 20, color: tuple = (255, 255, 0), width: int = 2):
    end_x = center[0] + math.cos(angle) * length
    end_y = center[1] + math.sin(angle) * length
    pygame.draw.line(screen, color, center, (end_x, end_y), width)