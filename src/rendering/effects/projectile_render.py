import pygame
from src.objects.weapons.projectile import Projectile
from src.core import config


class ProjectileRenderer:
    """
    View: Отрисовка снарядов.
    Содержит только визуальную логику (цвета, размеры, формы).
    НЕ содержит игровую логику или обновление состояния.
    """

    def __init__(self):
        # Цвета для разных типов снарядов (MVP - примитивы)
        self.colors = {
            'player': config.yellow,  # Пули игрока - жёлтые
            'enemy': config.red  # Пули врагов - красные
        }

    def render(self, screen: pygame.Surface, projectile: Projectile):
        """
        Отрисовка снаряда на экране.

        :param screen: Поверхность для отрисовки
        :param projectile: Снаряд для отрисовки
        """
        color = self.colors.get(projectile.owner_type, config.white)

        # Рисуем круг (снаряд)
        pygame.draw.circle(screen, color, (int(projectile.x), int(projectile.y)),projectile.radius)

        # Опционально: обводка для лучшей видимости
        pygame.draw.circle(screen,
            config.black,
            (int(projectile.x), int(projectile.y)),
            projectile.radius,
            1  # толщина обводки
        )