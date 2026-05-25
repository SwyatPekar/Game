"""
Утилиты для рендеринга.
"""
import pygame
import math


def rotate_surface(surface: pygame.Surface, angle: float) -> pygame.Surface:
    """
    Поворот поверхности с сохранением центра

    Args:
        surface: Поверхность для поворота
        angle: Угол поворота в градусах

    Returns:
        Повернутая поверхность
    """
    return pygame.transform.rotate(surface, -angle)


def draw_direction_line(screen: pygame.Surface, center: tuple, angle: float,
                        length: int = 20, color: tuple = (255, 255, 0), width: int = 2):
    """
    Отрисовка линии направления

    Args:
        screen: Поверхность для отрисовки
        center: Центральная точка (x, y)
        angle: Угол в радианах
        length: Длина линии
        color: Цвет линии
        width: Толщина линии
    """
    end_x = center[0] + math.cos(angle) * length
    end_y = center[1] + math.sin(angle) * length
    pygame.draw.line(screen, color, center, (end_x, end_y), width)