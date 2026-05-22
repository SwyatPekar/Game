"""
Обработчик ввода.
Обрабатывает события pygame (клавиатура, мышь, выход).
"""

import pygame


class InputHandler:
    """Централизованный обработчик пользовательского ввода."""
    
    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = [False, False, False]  # ЛКМ, СКМ, ПКМ
        self.quit_requested = False
        
        # События однократного действия (сбрасываются после обработки)
        self.shoot_pressed = False
        self.roll_pressed = False
    
    def handle_events(self):
        """
        Обрабатывает все события pygame.
        
        Returns:
            'quit' если запрошен выход, иначе None
        """
        self.shoot_pressed = False
        self.roll_pressed = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
                return 'quit'
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
                    return 'quit'
                # Перекат на пробел
                if event.key == pygame.K_SPACE:
                    self.roll_pressed = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    self.shoot_pressed = True
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
        
        # Обновляем состояние клавиш и мыши
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_buttons[0] = pygame.mouse.get_pressed()[0]
        
        return None
    
    def get_keys(self):
        """Возвращает текущее состояние клавиш."""
        return self.keys_pressed
    
    def get_mouse_pos(self):
        """Возвращает позицию мыши."""
        return self.mouse_pos
    
    def is_shoot_pressed(self):
        """Проверяет, была ли нажата кнопка стрельбы (однократно)."""
        return self.shoot_pressed
    
    def is_roll_pressed(self):
        """Проверяет, была ли нажата кнопка переката (однократно)."""
        return self.roll_pressed