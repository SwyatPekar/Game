"""
Меню состояния.
Простое главное меню с кнопкой старта.
"""

import pygame
from src.core.config import Config


class MenuState:
    """Состояние главного меню."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_requested = False
    
    def handle_input(self, input_handler):
        """Обрабатывает ввод в меню."""
        keys = input_handler.get_keys()
        
        # Старт на Enter или ЛКМ
        if input_handler.is_shoot_pressed() or keys[pygame.K_RETURN]:
            self.start_requested = True
        
        # Выход на Escape
        if input_handler.quit_requested:
            return 'quit'
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление меню (пока пусто)."""
        pass
    
    def render(self, screen):
        """Отрисовка меню."""
        screen.fill(Config.COLOR_BG)
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 36)
        
        # Заголовок
        title_text = font_large.render("Mass Effect", True, Config.COLOR_UI_TEXT)
        subtitle_text = font_medium.render("They Will Not Break Us", True, Config.COLOR_PLAYER)
        
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3 + 50))
        
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Инструкция
        instruction_text = font_medium.render("Press ENTER or CLICK to Start", True, Config.COLOR_UI_TEXT)
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(instruction_text, instruction_rect)
        
        # Управление
        controls_font = pygame.font.Font(None, 24)
        controls = [
            "WASD - Move",
            "Mouse - Aim",
            "LMB - Shoot",
            "SPACE - Roll",
            "ESC - Quit"
        ]
        
        y_offset = self.screen_height // 2 + 80
        for control in controls:
            text = controls_font.render(control, True, (150, 150, 150))
            rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, rect)
            y_offset += 25
    
    def is_start_requested(self) -> bool:
        """Проверяет, запрошен ли старт игры."""
        return self.start_requested
