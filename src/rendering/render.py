import pygame
from abc import ABC, abstractmethod


class BaseRenderer(ABC):

    @abstractmethod
    def render(self, screen: pygame.Surface, entity):
        pass