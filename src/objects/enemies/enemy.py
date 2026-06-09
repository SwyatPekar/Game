import math
import random
import pygame
from collections import deque
from src.objects.entity import Entity
from src.systems.combat_system.melee_attack import MeleeAttack
from src.core import config
from src.systems.a_star import AStar


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
        self.detection_range = config.enemy_detection_range
        self.attack_range = stats['attack_range']
        self.attack_cooldown_timer = 0
        self.patrol_timer = config.enemy_patrol_timer
        self.patrol_direction = (1, 0)
        self.current_attack: MeleeAttack = None

        self.path = deque()
        self.path_timer = 0.0
        self.path_update_interval = 0.5
        self.current_target_tile = None
        self.last_position = (x, y)
        self.stuck_timer = 0.0

        self.facing_angle = 0  # <-- ДОБАВЛЕНО

    def get_enemy_stats(self, enemy_type: str) -> dict:
        return {
            'width': config.enemy_base_width,
            'height': config.enemy_base_height,
            'speed': config.enemy_base_speed,
            'health': config.enemy_base_health,
            'damage': config.enemy_base_damage,
            'attack_range': config.enemy_base_attack_range
        }

    def update(self, dt: float, player: Entity, walls: list, grid: list):
        if not self.is_alive:
            return

        self.current_attack = None
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt

        if player and player.is_alive:
            distance = self.distance_to(player)
            self._update_ai_state(distance)
            self._update_facing_angle(player)  # <-- ДОБАВЛЕНО
            self._execute_ai_behavior(dt, player, walls, grid)

    def _update_facing_angle(self, player: Entity):  # <-- ДОБАВЛЕН МЕТОД
        dx = player.x - (self.x + self.width / 2)
        dy = player.y - (self.y + self.height / 2)
        self.facing_angle = math.atan2(dy, dx)

    def _execute_ai_behavior(self, dt: float, player: Entity, walls: list, grid: list):
        if self.state == "chase":
            self._chase_player_smart(dt, player, walls, grid)
        elif self.state == "attack":
            self._attack_player(player)
        elif self.state == "patrol":
            self._patrol(dt, walls)

    def _chase_player(self, dt: float, player: Entity, walls: list):
        dx = player.x - self.x
        dy = player.y - self.y

        if dx != 0 or dy != 0:
            length = math.sqrt(dx ** 2 + dy ** 2)
            dx, dy = dx / length, dy / length
            self._move_with_collision(dx, dy, dt, walls)

    def _chase_player_smart(self, dt: float, player: Entity, walls: list, grid: list):
        self.path_timer -= dt
        target_tile = self._get_tile(player.x, player.y)

        if self.path_timer <= 0 or self.current_target_tile != target_tile:
            self.path_timer = self.path_update_interval
            self.current_target_tile = target_tile
            start_tile = self._get_tile(self.x, self.y)
            self.path = deque(AStar.find_path(grid, start_tile, target_tile))

        distance_moved = math.sqrt((self.x - self.last_position[0]) ** 2 + (self.y - self.last_position[1]) ** 2)
        self.last_position = (self.x, self.y)

        if distance_moved < 1:
            self.stuck_timer += dt
        else:
            self.stuck_timer = 0.0

        if self.stuck_timer > 0.5:
            self.path.clear()
            self.stuck_timer = 0.0

        if len(self.path) > 1:
            target_tile_pos = self.path[1]
            target_x = target_tile_pos[0] * config.tile_size + config.tile_size / 2
            target_y = target_tile_pos[1] * config.tile_size + config.tile_size / 2

            dx = target_x - (self.x + self.width / 2)
            dy = target_y - (self.y + self.height / 2)
            distance_to_target = math.sqrt(dx ** 2 + dy ** 2)

            if distance_to_target < 15:
                self.path.popleft()
                return

            if dx != 0 or dy != 0:
                length = math.sqrt(dx ** 2 + dy ** 2)
                dx, dy = dx / length, dy / length
                self._move_with_collision(dx, dy, dt, walls)
        else:
            self._chase_player(dt, player, walls)

    def _get_tile(self, px: float, py: float) -> tuple:
        tx = int((px + self.width / 2) // config.tile_size)
        ty = int((py + self.height / 2) // config.tile_size)
        return (tx, ty)

    def _update_ai_state(self, distance: float):
        if distance <= self.attack_range:
            self.state = "attack"
        elif distance <= self.detection_range:
            self.state = "chase"
        else:
            self.state = "patrol"

    def _attack_player(self, player: Entity):
        if self.attack_cooldown_timer <= 0:
            self.current_attack = self.attack(player)
            self.attack_cooldown_timer = config.enemy_attack_cooldown

    def attack(self, target: Entity) -> MeleeAttack:
        return MeleeAttack(
            damage=self.damage,
            attack_range=self.attack_range,
            duration=0.2,
            is_melee=True
        )

    def _patrol(self, dt: float, walls: list):
        self.patrol_timer -= dt

        if self.patrol_timer <= 0:
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            length = math.sqrt(dx ** 2 + dy ** 2)
            if length > 0:
                self.patrol_direction = (dx / length, dy / length)
            self.patrol_timer = config.enemy_patrol_timer

        dx, dy = self.patrol_direction
        self._move_with_collision(dx, dy, dt, walls)

    def _move_with_collision(self, dx: float, dy: float, dt: float, walls: list):
        new_x = self.x + dx * self.speed * dt
        if not self._check_wall_collision(new_x, self.y, walls):
            self.x = new_x

        new_y = self.y + dy * self.speed * dt
        if not self._check_wall_collision(self.x, new_y, walls):
            self.y = new_y

    def _check_wall_collision(self, x: float, y: float, walls: list) -> bool:
        rect = pygame.Rect(x, y, self.width, self.height)
        return any(rect.colliderect(wall) for wall in walls)

    def get_color(self) -> tuple:
        return (255, 0, 0)