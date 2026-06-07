import pygame
import math


class Attack:
    def __init__(self, damage: int, range: float, duration: float = 0.1, is_melee: bool = True):
        self.damage = damage
        self.range = range
        self.duration = duration
        self.is_melee = is_melee
        self.is_active = True
        self.timer = duration

    def update(self, dt: float):
        self.timer -= dt
        if self.timer <= 0:
            self.is_active = False

    def get_hitbox(self, attacker_x: float, attacker_y: float, attacker_width: int,
                   attacker_height: int, facing_angle: float) -> pygame.Rect:
        center_x = attacker_x + attacker_width / 2
        center_y = attacker_y + attacker_height / 2

        attacker_radius = max(attacker_width, attacker_height) / 2

        offset_dist = attacker_radius + self.range / 2
        offset_x = math.cos(facing_angle) * offset_dist
        offset_y = math.sin(facing_angle) * offset_dist

        hitbox_x = center_x + offset_x - self.range / 2
        hitbox_y = center_y + offset_y - self.range / 2

        return pygame.Rect(hitbox_x, hitbox_y, self.range, self.range)