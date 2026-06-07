import math
import pygame
from src.objects.entity import Entity
from src.combat.attack import Attack
from src.core.config import enemy_detection_range, enemy_attack_cooldown, enemy_patrol_timer


class Enemy(Entity):
    def __init__(self, x: float, y: float, enemy_type: str):
        stats = self.get_enemy_stats(enemy_type)
        super().__init__(x, y, stats['width'], stats['height'], stats['speed'])

        self.enemy_type = enemy_type
        self.health = stats['health']
        self.max_health = stats['health']
        self.damage = stats['damage']
        self.speed = stats['speed']

        self.state = "patrol"
        self.target = None
        self.detection_range = enemy_detection_range
        self.attack_range = stats['attack_range']
        self.attack_cooldown_timer = 0
        self.patrol_timer = 0
        self.patrol_direction = (1, 0)

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': 32,
            'height': 32,
            'speed': 100,
            'health': 50,
            'damage': 10,
            'attack_range': 40
        }

    def update(self, dt: float, player: Entity, walls: list):
        if not self.is_alive:
            return

        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt

        if player and player.is_alive:
            distance = self.distance_to(player)
            self._update_ai_state(distance, player)
            self._execute_ai_behavior(dt, player, walls)

    def _update_ai_state(self, distance: float, player: Entity):
        if distance <= self.attack_range:
            self.state = "attack"
        elif distance <= self.detection_range:
            self.state = "chase"
        else:
            self.state = "patrol"

    def _execute_ai_behavior(self, dt: float, player: Entity, walls: list):
        if self.state == "chase":
            self._chase_player(dt, player, walls)
        elif self.state == "attack":
            self._attack_player(dt, player)
        elif self.state == "patrol":
            self._patrol(dt, walls)

    def _chase_player(self, dt: float, player: Entity, walls: list):
        dx = player.x - self.x
        dy = player.y - self.y

        if dx != 0 or dy != 0:
            length = math.sqrt(dx ** 2 + dy ** 2)
            dx, dy = dx / length, dy / length
            self._move_with_collision(dx, dy, dt, walls)

    def _attack_player(self, dt: float, player: Entity):
        if self.attack_cooldown_timer <= 0:
            if self.distance_to(player) <= self.attack_range:
                if not hasattr(player, 'invincible') or not player.invincible:
                    player.take_damage(self.damage)
                    print(f"Враг {self.enemy_type} нанёс {self.damage} урона! HP игрока: {player.health}")

            self.attack_cooldown_timer = enemy_attack_cooldown

    def attack(self, target: Entity) -> Attack:
        return Attack(
            damage=self.damage,
            range=self.attack_range,
            duration=0.2,
            is_melee=True
        )

    def _patrol(self, dt: float, walls: list):
        self.patrol_timer -= dt

        if self.patrol_timer <= 0:
            import random
            self.patrol_direction = (random.uniform(-1, 1), random.uniform(-1, 1))
            length = math.sqrt(self.patrol_direction[0] ** 2 + self.patrol_direction[1] ** 2)
            if length > 0:
                self.patrol_direction = (
                    self.patrol_direction[0] / length,
                    self.patrol_direction[1] / length
                )
            self.patrol_timer = enemy_patrol_timer

        dx, dy = self.patrol_direction
        self._move_with_collision(dx, dy, dt, walls)

    def _move_with_collision(self, dx: float, dy: float, dt: float, walls: list):
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt

        rect = pygame.Rect(new_x, new_y, self.width, self.height)
        collision = False

        for wall in walls:
            if rect.colliderect(wall):
                collision = True
                break

        if not collision:
            self.x = new_x
            self.y = new_y

    def draw(self, screen: pygame.Surface):
        color = self.get_color()
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        if self.health < self.max_health:
            self._draw_health_bar(screen)

    def get_color(self) -> tuple:
        return (255, 0, 0)

    def _draw_health_bar(self, screen: pygame.Surface):
        bar_width = self.width
        bar_height = 4
        bar_y = self.y - 8

        pygame.draw.rect(screen, (255, 0, 0), (self.x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, bar_y, health_width, bar_height))