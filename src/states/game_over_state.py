"""
Состояние Game Over.
Экран смерти с показом счета и кнопкой рестарта.
"""

import pygame
from src.core.config import Config


class GameOverState:
    """Состояние конца игры."""
    
    def __init__(self, screen_width: int, screen_height: int, final_score: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.final_score = final_score
        self.restart_requested = False
    
    def handle_input(self, input_handler):
        """Обрабатывает ввод на экране смерти."""
        keys = input_handler.get_keys()
        
        # Рестарт на Enter или ЛКМ
        if input_handler.is_shoot_pressed() or keys[pygame.K_RETURN]:
            self.restart_requested = True
        
        # Выход на Escape
        if input_handler.quit_requested:
            return 'quit'
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление (пока пусто)."""
        pass
    
    def render(self, screen):
        """Отрисовка экрана смерти."""
        # Полупрозрачный фон
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 36)
        
        # Заголовок GAME OVER
        game_over_text = font_large.render("GAME OVER", True, Config.COLOR_ENEMY)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        screen.blit(game_over_text, game_over_rect)
        
        # Счет
        score_text = font_medium.render(f"Final Score: {self.final_score}", True, Config.COLOR_UI_TEXT)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(score_text, score_rect)
        
        # Инструкция рестарта
        restart_text = font_medium.render("Press ENTER or CLICK to Restart", True, Config.COLOR_UI_TEXT)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)
        
        # Выход
        quit_text = font_medium.render("ESC - Quit to Menu", True, (150, 150, 150))
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 90))
        screen.blit(quit_text, quit_rect)
    
    def is_restart_requested(self) -> bool:
        """Проверяет, запрошен ли рестарт."""
        return self.restart_requested
    
    def get_final_score(self) -> int:
        """Возвращает финальный счет."""
        return self.final_score
