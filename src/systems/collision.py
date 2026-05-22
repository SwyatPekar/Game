"""
Система коллизий.
Обрабатывает столкновения между объектами (AABB метод).
"""

import pygame


class CollisionSystem:
    """Отвечает за проверку и обработку столкновений."""
    
    def __init__(self):
        pass
    
    def check_bullet_enemy_collisions(self, bullets: pygame.sprite.Group, enemies: pygame.sprite.Group) -> list:
        """
        Проверяет столкновения пуль с врагами.
        
        Returns:
            Список убитых врагов
        """
        killed_enemies = []
        
        for bullet in bullets:
            # Используем встроенный спрайт-коллизию
            hits = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hits:
                enemy.take_damage(bullet.damage)
                bullet.is_active = False
                
                if not enemy.is_alive():
                    killed_enemies.append(enemy)
        
        return killed_enemies
    
    def check_enemy_player_collisions(self, enemies: pygame.sprite.Group, player) -> list:
        """
        Проверяет столкновения врагов с игроком (атака).
        
        Returns:
            Список врагов, которые атаковали игрока
        """
        attackers = []
        
        for enemy in enemies:
            if enemy.can_attack_player():
                if pygame.sprite.collide_rect(enemy, player):
                    if player.take_damage(enemy.damage):
                        attackers.append(enemy)
        
        return attackers
    
    def check_bounds(self, entity, screen_width: int, screen_height: int) -> bool:
        """
        Проверяет, находится ли сущность в пределах экрана.
        
        Returns:
            True если в пределах, False если вышла за границы
        """
        return (0 <= entity.rect.left and 
                entity.rect.right <= screen_width and
                0 <= entity.rect.top and 
                entity.rect.bottom <= screen_height)
