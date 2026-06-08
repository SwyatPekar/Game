import random
import collections
import pygame
from src.core import config
from src.objects.player import Player


class LevelGenerator:
    @staticmethod
    def generate():
        width = config.map_width_tiles
        height = config.map_height_tiles
        grid = LevelGenerator._generate_city_grid(width, height)

        center_x, center_y = width // 2, height // 2
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                grid[center_y + dy][center_x + dx] = config.tile_empty

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

        player_x = center_x * config.tile_size + (config.tile_size - config.player_width) // 2
        player_y = center_y * config.tile_size + (config.tile_size - config.player_height) // 2
        player = Player(player_x, player_y)

        return player, walls, grid

    @staticmethod
    def _generate_city_grid(width, height):
        grid = [[config.tile_empty for _ in range(width)] for _ in range(height)]
        blocks_x = max(2, width // 10)
        blocks_y = max(2, height // 10)

        block_width = width // blocks_x
        block_height = height // blocks_y

        margin_x = max(1, block_width // 4)
        margin_y = max(1, block_height // 4)

        for by in range(blocks_y):
            for bx in range(blocks_x):
                block_x_start = bx * block_width
                block_y_start = by * block_height
                block_x_end = block_x_start + block_width
                block_y_end = block_y_start + block_height

                available_width = block_width - margin_x * 2
                available_height = block_height - margin_y * 2

                if available_width < 3 or available_height < 3:
                    continue

                num_buildings = random.randint(1, 2)

                for _ in range(num_buildings):
                    max_building_width = min(available_width, block_width - margin_x * 2)
                    max_building_height = min(available_height, block_height - margin_y * 2)

                    if max_building_width < 3 or max_building_height < 3:
                        continue

                    building_width = random.randint(3, max_building_width)
                    building_height = random.randint(3, max_building_height)

                    building_x = random.randint(
                        block_x_start + margin_x,
                        max(block_x_start + margin_x, block_x_end - margin_x - building_width)
                    )
                    building_y = random.randint(
                        block_y_start + margin_y,
                        max(block_y_start + margin_y, block_y_end - margin_y - building_height)
                    )

                    for y in range(building_y, building_y + building_height):
                        for x in range(building_x, building_x + building_width):
                            if (y == building_y or y == building_y + building_height - 1 or
                                    x == building_x or x == building_x + building_width - 1):
                                grid[y][x] = config.tile_wall
                            else:
                                grid[y][x] = config.tile_empty

        return grid