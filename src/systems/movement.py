"""
Система движения.
Обрабатывает перемещение всех подвижных сущностей.
"""

import pygame


class MovementSystem:
    """Отвечает за обновление позиций всех объектов."""
    
    def __init__(self):
        pass
    
    def update(self, entities: list, dt: float, keys: tuple = None, mouse_pos: tuple = None):
        """
        Обновляет позиции сущностей.
        
        Args:
            entities: Список сущностей для обновления
            dt: Delta time (время между кадрами)
            keys: Состояние клавиш (только для игрока)
            mouse_pos: Позиция мыши (только для игрока)
        """
        for entity in entities:
            if hasattr(entity, 'update'):
                # Если это игрок - передаем ввод
                from src.entities.player import Player
                if isinstance(entity, Player):
                    entity.update(dt, keys, mouse_pos)
                else:
                    # Враги и пули обновляются без ввода
                    entity.update(dt)
