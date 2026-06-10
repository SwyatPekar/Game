import collections
import pygame
from src.core import config
from src.objects.player import Player
from src.systems.level_generator_system.city_generator import CityGenerator
from src.systems.level_generator_system.destruction_engine import DestructionEngine
from src.systems.level_generator_system.cover_placer import CoverPlacer


class LevelGenerator:
    @staticmethod
    def generate():
        width = config.map_width_tiles
        height = config.map_height_tiles

        grid = CityGenerator.generate(width, height)

        grid = DestructionEngine.apply(grid, width, height, destruction_level=0.3)

        CityGenerator._ensure_building_exits(grid, width, height)

        CoverPlacer.place_all(grid, width, height, destruction_level=0.3)

        LevelGenerator._clear_center(grid, width, height)

        LevelGenerator._remove_unreachable_areas(grid, width, height)

        return LevelGenerator._create_walls_and_player(grid, width, height)

    @staticmethod
    def _clear_center(grid, width, height):
        center_x, center_y = width // 2, height // 2
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                grid[center_y + dy][center_x + dx] = config.tile_empty

    @staticmethod
    def _remove_unreachable_areas(grid, width, height):
        center_x, center_y = width // 2, height // 2
        visited = set()
        queue = collections.deque([(center_x, center_y)])
        visited.add((center_x, center_y))

        while queue:
            cx, cy = queue.popleft()
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    if grid[ny][nx] != config.tile_wall:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        for y in range(height):
            for x in range(width):
                if (x, y) not in visited:
                    grid[y][x] = config.tile_wall

    @staticmethod
    def _create_walls_and_player(grid, width, height):
        walls = []
        for y in range(height):
            for x in range(width):
                if grid[y][x] == config.tile_wall:
                    rect = pygame.Rect(
                        x * config.tile_size,
                        y * config.tile_size,
                        config.tile_size,
                        config.tile_size
                    )
                    walls.append(rect)

        center_x, center_y = width // 2, height // 2
        player_x = center_x * config.tile_size + (config.tile_size - config.player_width) // 2
        player_y = center_y * config.tile_size + (config.tile_size - config.player_height) // 2
        player = Player(player_x, player_y)

        return player, walls, grid