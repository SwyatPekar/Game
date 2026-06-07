import math
import pygame


class Projectile:
    def __init__(self, x: float, y: float, angle: float, speed: float, damage: int, owner_type: str):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.owner_type = owner_type

        self.radius = 4
        self.is_active = True

    def update(self, dt: float):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )