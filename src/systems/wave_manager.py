import pygame
import random
from src.core import config
from src.objects.enemies.husk import Husk


class WaveManager:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.current_wave = 0
        self.state = "WAITING"

        self.active_enemies = []
        self.spawn_queue = []

        self.timer = 0.0
        self.score = 0

        self.spawn_points = [
            (100, 100), (window_width - 100, 100),
            (100, window_height - 100), (window_width - 100, window_height - 100),
            (window_width // 2, 50), (window_width // 2, window_height - 50)
        ]

        self.enemy_factory = {
            "husk": Husk,
        }

    def start_game(self):
        self.current_wave = 1
        self._prepare_wave()
        self.state = "SPAWNING"

    def reset(self):
        self.current_wave = 0
        self.state = "WAITING"
        self.active_enemies = []
        self.spawn_queue = []
        self.timer = 0.0
        self.score = 0

    def _prepare_wave(self):
        count = config.initial_enemies_count + (self.current_wave * config.enemies_increment)
        self.spawn_queue = ["husk"] * count

    def update(self, dt: float, walls: list, grid: list):
        self.active_enemies = [e for e in self.active_enemies if e.is_alive]

        self.timer += dt

        if self.state == "SPAWNING":
            self._handle_spawning(dt, walls, grid)
        elif self.state == "FIGHTING":
            self._handle_fighting()
        elif self.state == "RESTING":
            self._handle_resting()

    def _handle_spawning(self, dt: float, walls: list, grid: list):
        if self.timer >= config.wave_spawn_interval:
            self.timer -= config.wave_spawn_interval

            if self.spawn_queue:
                enemy_type = self.spawn_queue.pop(0)
                enemy = self._spawn_enemy(enemy_type, walls, grid)
                if enemy:
                    self.active_enemies.append(enemy)
            else:
                self.state = "FIGHTING"
                self.timer = 0.0

    def _handle_fighting(self):
        if not self.active_enemies:
            self.state = "RESTING"
            self.timer = 0.0
            self.score += self.current_wave * 100

    def _handle_resting(self):
        if self.timer >= config.wave_rest_duration:
            self.current_wave += 1
            self._prepare_wave()
            self.state = "SPAWNING"
            self.timer = 0.0

    def _spawn_enemy(self, enemy_type: str, walls: list, grid: list):
        max_attempts = 10

        enemy_class = self.enemy_factory.get(enemy_type, Husk)

        temp_enemy = enemy_class(0, 0)
        w, h = temp_enemy.width, temp_enemy.height

        for _ in range(max_attempts):
            x, y = random.choice(self.spawn_points)

            spawn_x = x - w // 2
            spawn_y = y - h // 2

            enemy_rect = pygame.Rect(spawn_x, spawn_y, w, h)

            if not any(enemy_rect.colliderect(wall) for wall in walls):
                return enemy_class(spawn_x, spawn_y)

        return None

    def get_enemies(self) -> list:
        return self.active_enemies

    def get_wave_info(self) -> dict:
        return {
            "wave": self.current_wave,
            "state": self.state,
            "timer": self.timer,
            "score": self.score
        }