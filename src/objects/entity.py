import pygame
import math


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
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, dt: float, *args, **kwargs):
        pass

    def draw(self, screen: pygame.Surface, renderer=None):
        if renderer:
            renderer.render(screen, self)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        self.is_alive = False

    def check_collision(self, other: 'Entity') -> bool:
        return self.get_rect().colliderect(other.get_rect())

    def distance_to(self, other: 'Entity') -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

