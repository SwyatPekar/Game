"""
Класс игрока (Боец N7).
Отвечает за состояние игрока: здоровье, позицию, скорость, кулдауны.
"""

import pygame
from src.core.config import Config


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        # Визуал: синий квадрат (прототип)
        self.image = pygame.Surface((Config.PLAYER_SIZE, Config.PLAYER_SIZE))
        self.image.fill(Config.COLOR_PLAYER)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Характеристики
        self.speed = Config.PLAYER_SPEED
        self.max_health = Config.PLAYER_MAX_HEALTH
        self.current_health = self.max_health
        
        # Состояния
        self.is_rolling = False
        self.roll_timer = 0
        self.roll_cooldown = 0
        
        # Направление стрельбы (последнее движение)
        self.facing_direction = pygame.math.Vector2(0, -1)  # По умолчанию вверх

    def update(self, dt: float, keys: tuple, mouse_pos: tuple):
        """Обновление состояния игрока."""
        self._handle_movement(keys, dt)
        self._handle_roll(dt)
        
        # Обновляем направление взгляда на основе позиции мыши
        if mouse_pos:
            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            if dx != 0 or dy != 0:
                self.facing_direction = pygame.math.Vector2(dx, dy).normalize()

    def _handle_movement(self, keys: tuple, dt: float):
        """Обработка ввода для перемещения."""
        move_x = 0
        move_y = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x = 1
            
        # Нормализация вектора движения (чтобы по диагонали не было быстрее)
        if move_x != 0 or move_y != 0:
            move_vector = pygame.math.Vector2(move_x, move_y).normalize()
            # Если не в перекате - двигаемся
            if not self.is_rolling:
                self.rect.x += move_vector.x * self.speed * dt * 60  # dt * 60 для кадровой независимости
                self.rect.y += move_vector.y * self.speed * dt * 60
                
                # Обновляем направление взгляда при движении, если мышь не двигается
                self.facing_direction = move_vector

    def _handle_roll(self, dt: float):
        """Логика переката (уклонения)."""
        if self.is_rolling:
            self.roll_timer -= dt
            if self.roll_timer <= 0:
                self.is_rolling = False
                self.roll_cooldown = Config.ROLL_COOLDOWN
        else:
            if self.roll_cooldown > 0:
                self.roll_cooldown -= dt

    def start_roll(self):
        """Начало переката."""
        if not self.is_rolling and self.roll_cooldown <= 0:
            self.is_rolling = True
            self.roll_timer = Config.ROLL_DURATION
            # Ускорение во время переката
            # (можно добавить рывок в направлении движения)

    def take_damage(self, amount: int):
        """Получение урона."""
        if not self.is_rolling:  # Неуязвимость во время переката
            self.current_health -= amount
            return True
        return False

    def is_alive(self) -> bool:
        """Проверка жизни."""
        return self.current_health > 0

    def get_health_percent(self) -> float:
        """Процент здоровья для HUD."""
        return max(0, self.current_health / self.max_health)
