import pygame
import math
from src.core import config

class Entity:
    def __init__(self, x: float, y: float, width: int, height: int, speed: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = 100
        self.max_health = 100
        self.is_alive = True

    def update(self, dt: float, *args, **kwargs):
        pass

    def draw(self, screen: pygame.Surface, renderers: dict = None):
        if renderers and 'entity' in renderers:
            renderers['entity'].render(screen, self)
        else:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, config.white, rect)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        self.is_alive = False

    def distance_to(self, other: 'Entity') -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

