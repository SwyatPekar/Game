import random
import pygame
from src.core import config
from src.objects.enemies.husk import Husk


class WaveManager:
    """
    System: Управление волнами врагов.
    Отвечает за тайминги, подсчет волн и спавн.
    """

    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.current_wave = 0
        self.state = "WAITING"  # WAITING, SPAWNING, FIGHTING, RESTING

        self.active_enemies = []
        self.spawn_queue = []  # Очередь врагов, которых нужно заспавнить

        self.timer = 0.0
        self.score = 0

        # Настройки спавна (зоны, куда безопасно спавнить врагов)
        # В будущем можно заменить на генератор случайных точек за пределами экрана
        self.spawn_points = [
            (100, 100), (window_width - 100, 100),
            (100, window_height - 100), (window_width - 100, window_height - 100),
            (window_width // 2, 50), (window_width // 2, window_height - 50)
        ]

    def start_game(self):
        """Запуск первой волны"""
        self.current_wave = 1
        self._prepare_wave()
        self.state = "SPAWNING"

    def _prepare_wave(self):
        """Генерация списка врагов для текущей волны"""
        self.spawn_queue = []

        # Простая формула сложности: Базовое кол-во + (НомерВолны * Прирост)
        count = config.initial_enemies_count + (self.current_wave * config.enemies_increment)

        # На старте только Хаски (потом добавим мародеров и т.д.)
        for _ in range(count):
            self.spawn_queue.append("husk")

    def update(self, dt: float, walls: list):
        """Основной цикл обновления волн"""
        self.timer += dt

        if self.state == "SPAWNING":
            self._handle_spawning(dt, walls)  # Передаём стены
        elif self.state == "FIGHTING":
            self._handle_fighting()
        elif self.state == "RESTING":
            self._handle_resting()

    def _handle_spawning(self, dt: float, walls: list):
        """Логика спавна: добавляем врагов по таймеру"""
        if self.timer >= config.wave_spawn_interval:
            if self.spawn_queue:
                enemy_type = self.spawn_queue.pop(0)
                enemy = self._spawn_enemy(enemy_type, walls)
                if enemy:  # Если спавн успешен
                    self.active_enemies.append(enemy)
                self.timer = 0.0
            else:
                # Очередь пуста -> переходим в бой
                self.state = "FIGHTING"
                self.timer = 0.0
                print(f"Волна {self.current_wave}: Все враги на карте!")

    def _handle_fighting(self):
        """Логика боя: проверка, остались ли враги"""
        # Фильтруем живых врагов
        alive_enemies = [e for e in self.active_enemies if e.is_alive]
        self.active_enemies = alive_enemies  # Очистка списка от мертвых

        if not alive_enemies:
            self.state = "RESTING"
            self.timer = 0.0
            self.score += self.current_wave * 100  # Бонус за волну
            print(f"Волна {self.current_wave} пройдена! Отдых...")

    def _handle_resting(self):
        """Логика отдыха: таймер до следующей волны"""
        if self.timer >= config.wave_rest_duration:
            self.current_wave += 1
            self._prepare_wave()
            self.state = "SPAWNING"
            self.timer = 0.0
            print(f"Начинается волна {self.current_wave}!")

    def _spawn_enemy(self, enemy_type: str):
        """Фабрика спавна врагов"""
        # Выбираем случайную точку спавна
        x, y = random.choice(self.spawn_points)

        if enemy_type == "husk":
            return Husk(x, y)
        # elif enemy_type == "marauder": ...
        else:
            return Husk(x, y)  # Fallback

    def _spawn_enemy(self, enemy_type: str, walls: list):
        """Фабрика спавна врагов с проверкой коллизий"""
        max_attempts = 10  # Сколько раз пробуем найти свободное место

        for _ in range(max_attempts):
            # Выбираем случайную точку спавна
            x, y = random.choice(self.spawn_points)

            # Создаём временный прямоугольник врага
            if enemy_type == "husk":
                # Размеры хаска (28x28 из husk.py)
                enemy_rect = pygame.Rect(x - 14, y - 14, 28, 28)
            else:
                enemy_rect = pygame.Rect(x - 16, y - 16, 32, 32)

            # Проверяем коллизии со стенами
            collision = False
            for wall in walls:
                if enemy_rect.colliderect(wall):
                    collision = True
                    break

            # Если коллизий нет - спавним врага
            if not collision:
                if enemy_type == "husk":
                    return Husk(x, y)
                else:
                    return Husk(x, y)

        # Если не нашли место за max_attempts - возвращаем None
        print(f"Warning: Could not spawn {enemy_type} - all positions blocked")
        return None

    def get_enemies(self) -> list:
        """Возвращает список ТОЛЬКО живых врагов для GameEngine"""
        # Фильтруем мёртвых врагов
        self.active_enemies = [e for e in self.active_enemies if e.is_alive]
        return self.active_enemies

    def get_wave_info(self) -> dict:
        """Информация для HUD"""
        return {
            "wave": self.current_wave,
            "state": self.state,
            "timer": self.timer,
            "score": self.score
        }