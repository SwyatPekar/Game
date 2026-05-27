import pygame
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class BaseRenderer(ABC, Generic[T]):
    """Базовый абстрактный класс для всех рендереров."""

    @abstractmethod
    def render(self, screen: pygame.Surface, entity: T):
        """Отрисовывает сущность на экране."""
        pass