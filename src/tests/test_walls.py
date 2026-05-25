"""
Генерация тестовых стен для проверки коллизий.
"""
import pygame
from src.core import config


def create_test_walls() -> list[pygame.Rect]:
    """
    Создаёт набор тестовых препятствий.
    Используется только на этапе разработки.
    """
    w, h = config.window_width, config.window_height

    return [
        # Границы экрана
        pygame.Rect(0, 0, 20, h),  # Левая
        pygame.Rect(w - 20, 0, 20, h),  # Правая
        pygame.Rect(0, 0, w, 20),  # Верхняя
        pygame.Rect(0, h - 20, w, 20),  # Нижняя

        # Внутренние препятствия
        pygame.Rect(100, 100, 200, 20),
        pygame.Rect(500, 300, 20, 200),
        pygame.Rect(300, 500, 200, 20),
    ]