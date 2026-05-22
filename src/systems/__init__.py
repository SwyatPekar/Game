"""
Системы игры.
Модуль для логики обработки движения, коллизий, боя и волн.
"""

from .movement import MovementSystem
from .collision import CollisionSystem
from .combat import CombatSystem
from .wave import WaveSystem

__all__ = ['MovementSystem', 'CollisionSystem', 'CombatSystem', 'WaveSystem']
