import pygame
import math


class MeleeAttack:
    def __init__(self, damage: int, attack_range: float, duration: float = 0.1):
        self.damage = damage
        self.attack_range = attack_range
        self.duration = duration
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

        offset_x = math.cos(facing_angle) * (self.attack_range / 2)
        offset_y = math.sin(facing_angle) * (self.attack_range / 2)

        hitbox_x = center_x + offset_x - self.attack_range / 2
        hitbox_y = center_y + offset_y - self.attack_range / 2

        return pygame.Rect(hitbox_x, hitbox_y, self.attack_range, self.attack_range)