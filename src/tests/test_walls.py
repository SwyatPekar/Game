import pygame
from src.core import config


def create_test_walls() -> list[pygame.Rect]:
    w, h = config.window_width, config.window_height

    return [
        pygame.Rect(0, 0, 20, h),
        pygame.Rect(w - 20, 0, 20, h),
        pygame.Rect(0, 0, w, 20),
        pygame.Rect(0, h - 20, w, 20),

        pygame.Rect(100, 100, 200, 20),
        pygame.Rect(500, 300, 20, 200),
        pygame.Rect(300, 500, 200, 20),
    ]