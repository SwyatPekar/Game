"""
Класс врага (силы Жнецов).
Базовая реализация ИИ: преследование игрока.
"""

import pygame
from src.core.config import Config


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, player_target: pygame.sprite.Sprite = None):
        super().__init__()
        # Визуал: красный прямоугольник (прототип)
        self.image = pygame.Surface((Config.ENEMY_SIZE, Config.ENEMY_SIZE))
        self.image.fill(Config.COLOR_ENEMY)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Характеристики (базовые, можно переопределять для типов врагов)
        self.speed = Config.ENEMY_SPEED
        self.max_health = Config.ENEMY_MAX_HEALTH
        self.current_health = self.max_health
        self.damage = Config.ENEMY_DAMAGE
        
        # Ссылка на игрока для преследования
        self.player_target = player_target
        
        # Состояния
        self.is_attacking = False
        self.attack_cooldown = 0

    def set_target(self, player: pygame.sprite.Sprite):
        """Установка цели для преследования."""
        self.player_target = player

    def update(self, dt: float):
        """Обновление состояния врага."""
        if self.player_target and self.player_target.is_alive():
            self._chase_player(dt)
        
        # Кулдаун атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def _chase_player(self, dt: float):
        """Простое преследование игрока."""
        dx = self.player_target.rect.centerx - self.rect.centerx
        dy = self.player_target.rect.centery - self.rect.centery
        distance = pygame.math.Vector2(dx, dy).length()
        
        # Если далеко - идем к игроку
        if distance > Config.ENEMY_ATTACK_RANGE:
            direction = pygame.math.Vector2(dx, dy).normalize()
            self.rect.x += direction.x * self.speed * dt * 60
            self.rect.y += direction.y * self.speed * dt * 60
        else:
            # Если близко - атакуем
            self._try_attack(dt)

    def _try_attack(self, dt: float):
        """Попытка атаки игрока."""
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            # Наносим урон (в реальной игре это должно обрабатываться в CombatSystem)
            self.attack_cooldown = Config.ENEMY_ATTACK_COOLDOWN
            self.is_attacking = False

    def take_damage(self, amount: int):
        """Получение урона."""
        self.current_health -= amount

    def is_alive(self) -> bool:
        """Проверка жизни."""
        return self.current_health > 0

    def can_attack_player(self) -> bool:
        """Проверка возможности атаки."""
        return (self.player_target and 
                self.player_target.is_alive() and
                self.attack_cooldown <= 0 and
                pygame.math.Vector2(
                    self.player_target.rect.centerx - self.rect.centerx,
                    self.player_target.rect.centery - self.rect.centery
                ).length() <= Config.ENEMY_ATTACK_RANGE)
