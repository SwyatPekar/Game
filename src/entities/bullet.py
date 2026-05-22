"""
Класс пули.
Отвечает за движение снаряда и время жизни.
"""

import pygame
from src.core.config import Config


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: pygame.math.Vector2, damage: int = Config.BULLET_DAMAGE):
        super().__init__()
        # Визуал: маленький желтый круг (пуля)
        self.image = pygame.Surface((Config.BULLET_SIZE, Config.BULLET_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, Config.COLOR_BULLET, 
                          (Config.BULLET_SIZE // 2, Config.BULLET_SIZE // 2), 
                          Config.BULLET_SIZE // 2)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Параметры
        self.direction = direction.normalize() if direction.length() > 0 else pygame.math.Vector2(0, -1)
        self.speed = Config.BULLET_SPEED
        self.damage = damage
        self.life_time = Config.BULLET_LIFETIME
        self.is_active = True

    def update(self, dt: float):
        """Обновление позиции пули."""
        # Движение
        self.rect.x += self.direction.x * self.speed * dt * 60
        self.rect.y += self.direction.y * self.speed * dt * 60
        
        # Время жизни
        self.life_time -= dt
        if self.life_time <= 0:
            self.is_active = False

    def is_out_of_bounds(self, screen_width: int, screen_height: int) -> bool:
        """Проверка выхода за границы экрана."""
        return (self.rect.right < 0 or 
                self.rect.left > screen_width or 
                self.rect.bottom < 0 or 
                self.rect.top > screen_height)
