import random
import pygame
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

    def start_game(self):
        self.current_wave = 1
        self._prepare_wave()
        self.state = "SPAWNING"

    def _prepare_wave(self):
        self.spawn_queue = []

        count = config.initial_enemies_count + (self.current_wave * config.enemies_increment)

        for _ in range(count):
            self.spawn_queue.append("husk")

    def update(self, dt: float, walls: list):
        self.timer += dt

        if self.state == "SPAWNING":
            self._handle_spawning(dt, walls)
        elif self.state == "FIGHTING":
            self._handle_fighting()
        elif self.state == "RESTING":
            self._handle_resting()

    def _handle_spawning(self, dt: float, walls: list):
        if self.timer >= config.wave_spawn_interval:
            if self.spawn_queue:
                enemy_type = self.spawn_queue.pop(0)
                enemy = self._spawn_enemy(enemy_type, walls)
                if enemy:
                    self.active_enemies.append(enemy)
                self.timer = 0.0
            else:
                self.state = "FIGHTING"
                self.timer = 0.0
                print(f"Волна {self.current_wave}: Все враги на карте!")

    def _handle_fighting(self):
        alive_enemies = [e for e in self.active_enemies if e.is_alive]
        self.active_enemies = alive_enemies

        if not alive_enemies:
            self.state = "RESTING"
            self.timer = 0.0
            self.score += self.current_wave * 100  # Бонус за волну
            print(f"Волна {self.current_wave} пройдена! Отдых...")

    def _handle_resting(self):
        if self.timer >= config.wave_rest_duration:
            self.current_wave += 1
            self._prepare_wave()
            self.state = "SPAWNING"
            self.timer = 0.0
            print(f"Начинается волна {self.current_wave}!")

    def _spawn_enemy(self, enemy_type: str):
        x, y = random.choice(self.spawn_points)

        if enemy_type == "husk":
            return Husk(x, y)
        else:
            return Husk(x, y)

    def _spawn_enemy(self, enemy_type: str, walls: list):
        max_attempts = 10

        for _ in range(max_attempts):
            x, y = random.choice(self.spawn_points)

            if enemy_type == "husk":
                enemy_rect = pygame.Rect(x - 14, y - 14, 28, 28)
            else:
                enemy_rect = pygame.Rect(x - 16, y - 16, 32, 32)

            collision = False
            for wall in walls:
                if enemy_rect.colliderect(wall):
                    collision = True
                    break

            if not collision:
                if enemy_type == "husk":
                    return Husk(x, y)
                else:
                    return Husk(x, y)

        print(f"Warning: Could not spawn {enemy_type} - all positions blocked")
        return None

    def get_enemies(self) -> list:
        self.active_enemies = [e for e in self.active_enemies if e.is_alive]
        return self.active_enemies

    def get_wave_info(self) -> dict:
        return {
            "wave": self.current_wave,
            "state": self.state,
            "timer": self.timer,
            "score": self.score
        }