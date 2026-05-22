"""
Боевая система.
Обрабатывает стрельбу, урон и смерть сущностей.
"""

import pygame
from src.entities.bullet import Bullet


class CombatSystem:
    """Отвечает за боевые взаимодействия."""
    
    def __init__(self):
        self.shoot_cooldown = 0
    
    def player_shoot(self, player, bullets_group: pygame.sprite.Group) -> bool:
        """
        Игрок стреляет в направлении взгляда.
        
        Returns:
            True если выстрел успешен, False если на кулдауне
        """
        if self.shoot_cooldown > 0:
            return False
        
        # Создаем пулю в центре игрока
        bullet = Bullet(
            player.rect.centerx,
            player.rect.centery,
            player.facing_direction
        )
        bullets_group.add(bullet)
        
        self.shoot_cooldown = 0.15  # Скорострельность (секунды между выстрелами)
        return True
    
    def update(self, dt: float):
        """Обновление кулдаунов."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
    
    def remove_dead_enemies(self, enemies: pygame.sprite.Group, killed_list: list):
        """Удаляет мертвых врагов из группы."""
        for enemy in killed_list:
            enemies.remove(enemy)
    
    def cleanup_bullets(self, bullets: pygame.sprite.Group, screen_width: int, screen_height: int):
        """Удаляет пули, которые улетели за экран или истекло время."""
        for bullet in bullets:
            if not bullet.is_active or bullet.is_out_of_bounds(screen_width, screen_height):
                bullets.remove(bullet)
