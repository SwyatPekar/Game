"""
Система волн.
Управляет спавном врагов и прогрессией сложности.
"""

import pygame
import random
from src.entities.enemy import Enemy
from src.core.config import Config


class WaveSystem:
    """Отвечает за управление волнами врагов."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.current_wave = 0
        self.enemies_spawned_in_wave = 0
        self.total_enemies_to_spawn = 0
        
        self.wave_timer = 0
        self.spawn_timer = 0
        self.is_wave_active = False
        self.is_waiting_for_wave = True
        
        # Зоны спавна (за пределами экрана)
        self.spawn_margin = 50
    
    def start_wave(self, wave_number: int):
        """Начинает новую волну."""
        self.current_wave = wave_number
        self.enemies_spawned_in_wave = 0
        self.total_enemies_to_spawn = (
            Config.WAVE_ENEMY_COUNT_BASE + 
            (wave_number - 1) * Config.WAVE_ENEMY_COUNT_INCREMENT
        )
        self.is_wave_active = True
        self.is_waiting_for_wave = False
        self.spawn_timer = 0
    
    def update(self, dt: float, enemies_group: pygame.sprite.Group, player):
        """
        Обновление системы волн.
        
        Returns:
            True если волна завершена, False иначе
        """
        if self.is_waiting_for_wave:
            self.wave_timer -= dt
            if self.wave_timer <= 0:
                self.start_wave(self.current_wave + 1)
            return False
        
        if not self.is_wave_active:
            return False
        
        # Спавн врагов
        if self.enemies_spawned_in_wave < self.total_enemies_to_spawn:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self._spawn_enemy(enemies_group, player)
                self.enemies_spawned_in_wave += 1
                self.spawn_timer = Config.WAVE_SPAWN_INTERVAL
        
        # Проверка завершения волны
        if len(enemies_group) == 0 and self.enemies_spawned_in_wave >= self.total_enemies_to_spawn:
            self.is_wave_active = False
            self.is_waiting_for_wave = True
            self.wave_timer = Config.WAVE_INITIAL_DELAY
            return True  # Волна завершена
        
        return False
    
    def _spawn_enemy(self, enemies_group: pygame.sprite.Group, player):
        """Спавнит одного врага в случайной точке за экраном."""
        # Выбираем случайную сторону для спавна
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            x = random.randint(0, self.screen_width)
            y = -self.spawn_margin
        elif side == 'bottom':
            x = random.randint(0, self.screen_width)
            y = self.screen_height + self.spawn_margin
        elif side == 'left':
            x = -self.spawn_margin
            y = random.randint(0, self.screen_height)
        else:  # right
            x = self.screen_width + self.spawn_margin
            y = random.randint(0, self.screen_height)
        
        enemy = Enemy(x, y, player)
        enemies_group.add(enemy)
    
    def get_wave_info(self) -> tuple:
        """
        Возвращает информацию о текущей волне.
        
        Returns:
            (номер_волны, врагов_осталось, всего_врагов)
        """
        if self.is_waiting_for_wave:
            return (self.current_wave + 1, 0, 0)
        
        enemies_remaining = self.total_enemies_to_spawn - self.enemies_spawned_in_wave + len([e for e in self._get_all_enemies()])
        return (self.current_wave, enemies_remaining, self.total_enemies_to_spawn)
    
    def _get_all_enemies(self):
        """Вспомогательный метод (заглушка, реально используется группа)."""
        return []
