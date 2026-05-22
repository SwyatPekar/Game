"""
Основное игровое состояние.
Содержит всю логику геймплея: игрок, враги, волны, HUD.
"""

import pygame
from src.core.config import Config
from src.entities.player import Player
from src.systems.movement import MovementSystem
from src.systems.collision import CollisionSystem
from src.systems.combat import CombatSystem
from src.systems.wave import WaveSystem


class GameState:
    """Состояние активной игры."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Группы спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Игрок
        self.player = Player(screen_width // 2, screen_height // 2)
        self.all_sprites.add(self.player)
        
        # Системы
        self.movement_system = MovementSystem()
        self.collision_system = CollisionSystem()
        self.combat_system = CombatSystem()
        self.wave_system = WaveSystem(screen_width, screen_height)
        
        # Счет и прогресс
        self.score = 0
        self.is_running = True
    
    def handle_input(self, input_handler):
        """Обрабатывает ввод для игровых действий."""
        # Стрельба
        if input_handler.is_shoot_pressed():
            self.combat_system.player_shoot(self.player, self.bullets)
        
        # Перекат
        if input_handler.is_roll_pressed():
            self.player.start_roll()
    
    def update(self, dt, input_handler):
        """Обновляет игровую логику."""
        keys = input_handler.get_keys()
        mouse_pos = input_handler.get_mouse_pos()
        
        # Движение
        all_entities = [self.player] + list(self.enemies) + list(self.bullets)
        self.movement_system.update(all_entities, dt, keys, mouse_pos)
        
        # Бой (кулдауны)
        self.combat_system.update(dt)
        
        # Волны
        wave_complete = self.wave_system.update(dt, self.enemies, self.player)
        if wave_complete:
            pass  # Можно добавить бонус за завершение волны
        
        # Коллизии
        killed_enemies = self.collision_system.check_bullet_enemy_collisions(
            self.bullets, self.enemies
        )
        
        if killed_enemies:
            for enemy in killed_enemies:
                self.score += 10  # Очки за убийство
            self.combat_system.remove_dead_enemies(self.enemies, killed_enemies)
        
        # Урон игроку
        self.collision_system.check_enemy_player_collisions(self.enemies, self.player)
        
        # Очистка пуль
        self.combat_system.cleanup_bullets(self.bullets, self.screen_width, self.screen_height)
        
        # Проверка смерти
        if not self.player.is_alive():
            self.is_running = False
    
    def render(self, screen):
        """Отрисовка игры."""
        # Фон
        screen.fill(Config.COLOR_BG)
        
        # Все спрайты
        self.all_sprites.draw(screen)
        self.bullets.draw(screen)
        self.enemies.draw(screen)
        
        # HUD
        self._draw_hud(screen)
    
    def _draw_hud(self, screen):
        """Отрисовка интерфейса."""
        font = pygame.font.Font(None, 36)
        
        # Полоска здоровья
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = 10
        
        # Фон полоски
        pygame.draw.rect(screen, Config.COLOR_HEALTH_BAR_BG, 
                        (health_x, health_y, health_width, health_height))
        
        # Заполнение (текущее HP)
        current_health_width = int(health_width * self.player.get_health_percent())
        pygame.draw.rect(screen, Config.COLOR_HEALTH_BAR_FG,
                        (health_x, health_y, current_health_width, health_height))
        
        # Рамка
        pygame.draw.rect(screen, Config.COLOR_UI_TEXT,
                        (health_x, health_y, health_width, health_height), 2)
        
        # Счет
        score_text = font.render(f"Score: {self.score}", True, Config.COLOR_UI_TEXT)
        screen.blit(score_text, (health_x, health_y + health_height + 5))
        
        # Волна
        wave_num, enemies_left, total_enemies = self.wave_system.get_wave_info()
        if enemies_left > 0 or total_enemies > 0:
            wave_text = font.render(f"Wave: {wave_num} | Enemies: {enemies_left}", True, Config.COLOR_UI_TEXT)
        else:
            wave_text = font.render(f"Wave: {wave_num} (Next soon)", True, Config.COLOR_UI_TEXT)
        screen.blit(wave_text, (screen_width - wave_text.get_width() - 10, 10))
    
    def get_score(self) -> int:
        """Возвращает текущий счет."""
        return self.score
    
    def is_game_over(self) -> bool:
        """Проверяет, закончилась ли игра."""
        return not self.is_running
