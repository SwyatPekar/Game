import math
import pygame
from src.core import config
from src.objects.entity import Entity
from src.objects.weapons.projectile import Projectile
from src.systems.combat_system.melee_attack import MeleeAttack
from src.core.input_handler import InputHandler

class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, config.player_width, config.player_height, config.player_speed)
        self.health = config.player_max_health
        self.max_health = config.player_max_health
        self.damage = config.player_damage
        self.roll_cooldown = 0
        self.invincibility_timer = 0
        self.roll_duration = 0
        self.is_rolling = False
        self.roll_speed = config.player_roll_speed
        self.roll_direction = (0, 0)
        self.invincible = False
        self.shoot_cooldown = 0.0
        self.shoot_cooldown_duration = 0.2
        self.facing_angle = 0

    def update(self, dt: float, input_handler: 'InputHandler', walls: list):
        if self.is_rolling:
            self._update_roll(dt, walls)
        else:
            self._handle_movement(input_handler, dt, walls)
            self._handle_rolling_input(input_handler)

        if self.roll_cooldown > 0:
            self.roll_cooldown -= dt

        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        self._update_facing_angle(input_handler.get_mouse_pos())

    def _handle_movement(self, input_handler: 'InputHandler', dt: float, walls: list):
        dx, dy = 0, 0

        if input_handler.is_key_pressed(pygame.K_w) or input_handler.is_key_pressed(pygame.K_UP): dy = -1
        if input_handler.is_key_pressed(pygame.K_s) or input_handler.is_key_pressed(pygame.K_DOWN): dy = 1
        if input_handler.is_key_pressed(pygame.K_a) or input_handler.is_key_pressed(pygame.K_LEFT): dx = -1
        if input_handler.is_key_pressed(pygame.K_d) or input_handler.is_key_pressed(pygame.K_RIGHT): dx = 1

        if dx != 0 or dy != 0:
            length = math.sqrt(dx ** 2 + dy ** 2)
            dx, dy = dx / length, dy / length

        self._move_with_collision(dx, dy, dt, walls)

    def _move_with_collision(self, dx: float, dy: float, dt: float, walls: list):
        intended_x = self.x + dx * self.speed * dt
        new_x = max(0, min(intended_x, config.window_width - self.width))
        if not self._check_wall_collision(new_x, self.y, walls):
            self.x = new_x

        intended_y = self.y + dy * self.speed * dt
        new_y = max(0, min(intended_y, config.window_height - self.height))
        if not self._check_wall_collision(self.x, new_y, walls):
            self.y = new_y

    def _check_wall_collision(self, x: float, y: float, walls: list) -> bool:
        rect = pygame.Rect(x, y, self.width, self.height)
        for wall in walls:
            if rect.colliderect(wall):
                return True
        return False

    def _handle_rolling_input(self, input_handler: 'InputHandler'):
        if not input_handler.is_key_pressed(pygame.K_LSHIFT) and not input_handler.is_key_pressed(pygame.K_RSHIFT):
            return

        if self.roll_cooldown <= 0:
            dx, dy = 0, 0
            if input_handler.is_key_pressed(pygame.K_w) or input_handler.is_key_pressed(pygame.K_UP): dy = -1
            if input_handler.is_key_pressed(pygame.K_s) or input_handler.is_key_pressed(pygame.K_DOWN): dy = 1
            if input_handler.is_key_pressed(pygame.K_a) or input_handler.is_key_pressed(pygame.K_LEFT): dx = -1
            if input_handler.is_key_pressed(pygame.K_d) or input_handler.is_key_pressed(pygame.K_RIGHT): dx = 1

            if dx == 0 and dy == 0:
                dx = math.cos(self.facing_angle)
                dy = math.sin(self.facing_angle)

            if dx != 0 or dy != 0:
                length = math.sqrt(dx ** 2 + dy ** 2)
                dx, dy = dx / length, dy / length
                self.start_roll(dx, dy)

    def start_roll(self, dx: float, dy: float):
        self.is_rolling = True
        self.roll_duration = config.player_roll_duration
        self.invincibility_timer = config.player_roll_invincibility
        self.roll_cooldown = config.player_roll_cooldown
        self.roll_direction = (dx, dy)
        self.invincible = True

    def _update_roll(self, dt: float, walls: list):
        self.roll_duration -= dt

        if self.roll_duration <= 0:
            self.is_rolling = False
        else:
            dx, dy = self.roll_direction
            new_x = self.x + dx * self.roll_speed * dt
            new_y = self.y + dy * self.roll_speed * dt

            if not self._check_wall_collision(new_x, self.y, walls):
                self.x = new_x
            if not self._check_wall_collision(self.x, new_y, walls):
                self.y = new_y

    def _update_facing_angle(self, mouse_pos: tuple):
        dx = mouse_pos[0] - (self.x + self.width / 2)
        dy = mouse_pos[1] - (self.y + self.height / 2)
        self.facing_angle = math.atan2(dy, dx)

    def draw(self, screen: pygame.Surface, renderers: dict = None):
        if renderers:
            if 'player' in renderers:
                renderers['player'].render(screen, self)
            if 'health_bar' in renderers:
                renderers['health_bar'].render(screen, self)
        else:
            pygame.draw.rect(screen, config.green, (self.x, self.y, self.width, self.height))

    def shoot(self) -> Projectile:
        if self.shoot_cooldown > 0:
            return None
        self.shoot_cooldown = self.shoot_cooldown_duration

        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        return Projectile(
            x=center_x,
            y=center_y,
            angle=self.facing_angle,
            speed=config.bullet_speed,
            damage=self.damage,
            owner_type='player'
        )

    def kick(self) -> MeleeAttack:
        return MeleeAttack(
            damage=config.player_kick_damage,
            attack_range=config.player_kick_range,
            duration=0.15,
            is_melee=True
        )