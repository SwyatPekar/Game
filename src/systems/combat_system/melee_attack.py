import pygame
import math

class MeleeAttack:
    def __init__(self, damage: int, attack_range: float, duration: float = 0.1, is_melee: bool = True,
                 attack_width: float = None):
        self.damage = damage
        self.attack_range = attack_range
        self.attack_width = attack_width if attack_width is not None else attack_range / 2
        self.duration = duration
        self.is_melee = is_melee
        self.is_active = True
        self.timer = duration
        self._hitbox = pygame.Rect(0, 0, 0, 0)

    def update(self, dt: float):
        self.timer = max(0.0, self.timer - dt)
        if self.timer <= 0:
            self.is_active = False

    def get_hitbox(self, attacker_x: float, attacker_y: float, attacker_width: int, attacker_height: int,
                   facing_angle: float) -> pygame.Rect:
        center_x = attacker_x + attacker_width / 2
        center_y = attacker_y + attacker_height / 2

        offset_x = math.cos(facing_angle) * (self.attack_range / 2)
        offset_y = math.sin(facing_angle) * (self.attack_range / 2)

        self._hitbox.x = int(center_x + offset_x - self.attack_range / 2)
        self._hitbox.y = int(center_y + offset_y - self.attack_width / 2)
        self._hitbox.w = int(self.attack_range)
        self._hitbox.h = int(self.attack_width)

        return self._hitbox