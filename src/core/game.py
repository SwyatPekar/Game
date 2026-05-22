"""
Игровой движок.
Управляет игровым циклом, состояниями и рендерингом.
"""

import sys
import pygame
from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, COLOR_BG
from src.core.input_handler import InputHandler
from src.states.menu_state import MenuState
from src.states.game_state import GameState
from src.states.game_over_state import GameOverState


class GameEngine:
    """Основной движок игры с управлением состояниями."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Иконка (если есть)
        try:
            icon = pygame.image.load('assets/images/icon.png')
            pygame.display.set_icon(icon)
        except FileNotFoundError:
            pass  # Иконка не обязательна
        
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0  # Delta time
        
        # Ввод
        self.input_handler = InputHandler()
        
        # Система состояний
        self.current_state = None
        self.state_stack = []
        
        # Запускаем с меню
        self.change_state(MenuState(WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def change_state(self, new_state):
        """Переключает текущее состояние."""
        self.current_state = new_state
    
    def run(self):
        """Основной игровой цикл."""
        while self.running:
            # Обработка событий
            action = self.input_handler.handle_events()
            
            if action == 'quit':
                self.running = False
                continue
            
            # Обновление состояния
            self.current_state.update(self.dt, self.input_handler)
            
            # Обработка ввода состояния
            state_action = self.current_state.handle_input(self.input_handler)
            if state_action == 'quit':
                self.running = False
                continue
            
            # Переходы между состояниями
            self._handle_state_transitions()
            
            # Рендеринг
            self.screen.fill(COLOR_BG)
            self.current_state.render(self.screen)
            pygame.display.flip()
            
            # Контроль FPS
            self.dt = self.clock.tick(FPS) / 1000.0  # Конвертируем в секунды
        
        self.cleanup()
    
    def _handle_state_transitions(self):
        """Обрабатывает переходы между состояниями."""
        if isinstance(self.current_state, MenuState):
            if self.current_state.is_start_requested():
                self.change_state(GameState(WINDOW_WIDTH, WINDOW_HEIGHT))
        
        elif isinstance(self.current_state, GameState):
            if self.current_state.is_game_over():
                score = self.current_state.get_score()
                self.change_state(GameOverState(WINDOW_WIDTH, WINDOW_HEIGHT, score))
        
        elif isinstance(self.current_state, GameOverState):
            if self.current_state.is_restart_requested():
                self.change_state(GameState(WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def cleanup(self):
        """Очистка ресурсов."""
        pygame.quit()
        sys.exit()
