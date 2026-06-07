import random
import pygame
from src.core import config
from src.objects.player import Player


class LevelGenerator:
    @staticmethod
    def generate():
        width = config.map_width_tiles
        height = config.map_height_tiles

        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    row.append(config.tile_wall)
                else:
                    rand = random.random()
                    if rand < 0.35:
                        row.append(config.tile_wall)
                    elif rand < 0.50:
                        row.append(config.tile_rubble)
                    else:
                        row.append(config.tile_empty)
            grid.append(row)

        for _ in range(4):
            new_grid = [row[:] for row in grid]
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    wall_neighbors = sum(
                        1 for dy in [-1, 0, 1] for dx in [-1, 0, 1]
                        if grid[y + dy][x + dx] == config.tile_wall
                    )
                    if grid[y][x] == config.tile_wall and wall_neighbors < 4:
                        new_grid[y][x] = config.tile_empty
                    elif grid[y][x] == config.tile_empty and wall_neighbors > 4:
                        new_grid[y][x] = config.tile_wall
            grid = new_grid

        center_x, center_y = width // 2, height // 2
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                grid[center_y + dy][center_x + dx] = config.tile_empty

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