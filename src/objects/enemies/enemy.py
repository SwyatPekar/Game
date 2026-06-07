import math
import random
import pygame
from src.objects.entity import Entity
from src.combat.attack import Attack
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
        self.current_attack: Attack = None

        self.path = []
        self.path_timer = 0.0
        self.path_update_interval = 0.5
        self.current_target_tile = None

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
            self._update_ai_state(distance, player)

            self._execute_ai_behavior(dt, player, walls, grid)

    def _execute_ai_behavior(self, dt: float, player: Entity, walls: list, grid: list):
        if self.state == "chase":
            self._chase_player_smart(dt, player, walls, grid)
        elif self.state == "attack":
            self._attack_player(dt, player)
        elif self.state == "patrol":
            self._patrol(dt, walls)

    def _chase_player_smart(self, dt: float, player: Entity, walls: list, grid: list):
        self.path_timer -= dt
        if self.path_timer <= 0 or self.current_target_tile != self._get_tile(player.x, player.y):
            self.path_timer = self.path_update_interval
            self.current_target_tile = self._get_tile(player.x, player.y)

            start_tile = self._get_tile(self.x, self.y)
            self.path = AStar.find_path(grid, start_tile, self.current_target_tile)

        if len(self.path) > 1:
            target_tile = self.path[1]

            target_x = target_tile[0] * config.tile_size + config.tile_size / 2
            target_y = target_tile[1] * config.tile_size + config.tile_size / 2

            dx = target_x - (self.x + self.width / 2)
            dy = target_y - (self.y + self.height / 2)

            if dx != 0 or dy != 0:
                length = math.sqrt(dx ** 2 + dy ** 2)
                dx, dy = dx / length, dy / length
                self._move_with_collision(dx, dy, dt, walls)

            if length < 5:
                self.path.pop(0)
        else:
            self._chase_player(dt, player, walls)

    def _get_tile(self, px: float, py: float) -> tuple:
        tx = int((px + self.width / 2) // config.tile_size)
        ty = int((py + self.height / 2) // config.tile_size)
        return (tx, ty)

    def _update_ai_state(self, distance: float, player: Entity):
        if distance <= self.attack_range:
            self.state = "attack"
        elif distance <= self.detection_range:
            self.state = "chase"
        else:
            self.state = "patrol"

    def _attack_player(self, dt: float, player: Entity):
        if self.attack_cooldown_timer <= 0:
            if self.distance_to(player) <= self.attack_range:
                # Вместо прямого урона создаем объект атаки
                self.current_attack = self.attack(player)

            self.attack_cooldown_timer = config.enemy_attack_cooldown

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
            self.patrol_direction = (random.uniform(-1, 1), random.uniform(-1, 1))
            length = math.sqrt(self.patrol_direction[0] ** 2 + self.patrol_direction[1] ** 2)
            if length > 0:
                self.patrol_direction = (
                    self.patrol_direction[0] / length,
                    self.patrol_direction[1] / length
                )
            self.patrol_timer = config.enemy_patrol_timer

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

    def draw(self, screen: pygame.Surface, renderers: dict = None):
        color = self.get_color()
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        if self.health < self.max_health and renderers and 'health_bar' in renderers:
            renderers['health_bar'].render(screen, self, is_enemy=True)

        if config.debug_mode:
            center_x = int(self.x + self.width / 2)
            center_y = int(self.y + self.height / 2)

            if config.show_ai_states:
                font = pygame.font.SysFont("Arial", 12)
                text = font.render(self.state, True, config.white)
                screen.blit(text, (self.x, self.y - 20))

                pygame.draw.circle(screen, config.cyan, (center_x, center_y), int(self.detection_range), 1)

            if config.show_collision_boxes:
                pygame.draw.circle(screen, config.yellow, (center_x, center_y), int(self.attack_range), 1)
                pygame.draw.rect(screen, config.red, self.get_rect(), 1)

    def get_color(self) -> tuple:
        return (255, 0, 0)

    def _draw_health_bar(self, screen: pygame.Surface):
        bar_width = self.width
        bar_height = config.health_bar_height_enemy
        bar_y = self.y - config.health_bar_offset_y_enemy

        pygame.draw.rect(screen, config.red, (self.x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, config.green, (self.x, bar_y, health_width, bar_height))