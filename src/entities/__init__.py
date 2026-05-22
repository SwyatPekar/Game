"""
Модуль сущностей игры.
Содержит базовые классы для игровых объектов.
"""

from .player import Player
from .enemy import Enemy
from .bullet import Bullet

__all__ = ['Player', 'Enemy', 'Bullet']
