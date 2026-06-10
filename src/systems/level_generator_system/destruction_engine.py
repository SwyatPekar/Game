import random
from src.core import config


class DestructionEngine:
    @staticmethod
    def apply(grid, width, height, destruction_level=0.3):
        DestructionEngine._apply_explosions(grid, width, height, destruction_level)
        DestructionEngine._destroy_walls_smartly(grid, width, height, destruction_level)
        DestructionEngine._cleanup_isolated_walls(grid, width, height)
        return grid

    @staticmethod
    def _apply_explosions(grid, width, height, destruction_level):
        explosion_count = int(8 * destruction_level)
        for _ in range(explosion_count):
            cx = random.randint(5, width - 6)
            cy = random.randint(5, height - 6)
            radius = random.randint(2, 5)

            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        x, y = cx + dx, cy + dy
                        if 0 <= x < width and 0 <= y < height:
                            dist = (dx * dx + dy * dy) ** 0.5
                            if dist < radius * 0.3:
                                grid[y][x] = config.tile_empty
                            elif dist < radius * 0.6:
                                if random.random() < 0.5:
                                    grid[y][x] = config.tile_empty

    @staticmethod
    def _destroy_walls_smartly(grid, width, height, destruction_level):
        for y in range(2, height - 2):
            for x in range(2, width - 2):
                if grid[y][x] == config.tile_wall:
                    DestructionEngine._process_wall_by_neighbors(
                        grid, x, y, width, height, destruction_level
                    )

    @staticmethod
    def _process_wall_by_neighbors(grid, x, y, width, height, destruction_level):
        wall_neighbors = sum(
            1 for dy in range(-1, 2) for dx in range(-1, 2)
            if (dx != 0 or dy != 0) and
            0 <= y + dy < height and 0 <= x + dx < width and
            grid[y + dy][x + dx] == config.tile_wall
        )

        removal_probs = {
            0: 1.0, 1: 0.9, 2: 0.3,
            3: destruction_level * 0.15,
            4: destruction_level * 0.1,
            5: destruction_level * 0.05,
            6: destruction_level * 0.03,
            7: destruction_level * 0.02,
            8: 0.0,
        }

        prob = removal_probs.get(wall_neighbors, 0)
        if random.random() < prob:
            grid[y][x] = config.tile_empty

    @staticmethod
    def _cleanup_isolated_walls(grid, width, height):
        for _ in range(3):
            to_remove = []
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if grid[y][x] == config.tile_wall:
                        wall_neighbors = sum(
                            1 for dy in range(-1, 2) for dx in range(-1, 2)
                            if grid[y + dy][x + dx] == config.tile_wall
                        )
                        if wall_neighbors <= 1:
                            to_remove.append((x, y))

            for x, y in to_remove:
                grid[y][x] = config.tile_empty