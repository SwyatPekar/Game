import random
from src.core import config


class CoverPlacer:
    BARRICADE_PATTERNS = {
        'horizontal': lambda x, y: [(x, y), (x + 1, y), (x + 2, y)],
        'vertical': lambda x, y: [(x, y), (x, y + 1), (x, y + 2)],
        'L': lambda x, y: [
            (x, y), (x + 1, y), (x + 2, y),
            (x, y + 1), (x, y + 2)
        ],
        'corner': lambda x, y: [(x, y), (x + 1, y), (x, y + 1)],
        'car': lambda x, y: [
            (x + dx, y + dy) for dy in range(2) for dx in range(3)
        ],
        'diagonal': lambda x, y: [(x, y), (x + 1, y + 1), (x + 2, y + 2)],
        'u_shape': lambda x, y: [
            (x, y), (x + 1, y), (x + 2, y), (x + 3, y),
            (x, y + 1), (x + 3, y + 1)
        ],
        'long_wall': lambda x, y: [(x + i, y) for i in range(5)],
    }

    BARRICADE_SIZES = {
        'horizontal': (3, 1),
        'vertical': (1, 3),
        'L': (3, 3),
        'corner': (2, 2),
        'car': (3, 2),
        'diagonal': (3, 3),
        'u_shape': (4, 2),
        'long_wall': (5, 1),
    }

    ISLAND_PATTERNS = {
        'small_cluster': lambda x, y: [
            (x + dx, y + dy)
            for dy in range(random.choice([2, 3]))
            for dx in range(random.choice([2, 3]))
            if random.random() < 0.6
        ],
        'line_h': lambda x, y: [(x + i, y) for i in range(random.randint(3, 4))],
        'line_v': lambda x, y: [(x, y + i) for i in range(random.randint(3, 4))],
        'cross': lambda x, y: [
            (x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)
        ],
        'square': lambda x, y: [
            (x + dx, y + dy) for dy in range(3) for dx in range(3)
            if not (dy == 1 and dx == 1)
        ],
    }

    @staticmethod
    def place_all(grid, width, height, destruction_level):
        CoverPlacer._place_street_barricades(grid, width, height, destruction_level)
        CoverPlacer._add_cover_islands(grid, width, height, destruction_level)

    @staticmethod
    def _place_street_barricades(grid, width, height, destruction_level):
        barricade_count = int(45 * destruction_level)
        placed = 0
        attempts = 0
        max_attempts = barricade_count * 3

        while placed < barricade_count and attempts < max_attempts:
            if CoverPlacer._try_place_barricade(grid, width, height):
                placed += 1
            attempts += 1

    @staticmethod
    def _try_place_barricade(grid, width, height):
        for _ in range(50):
            x = random.randint(4, width - 5)
            y = random.randint(4, height - 4)

            if grid[y][x] != config.tile_empty:
                continue

            barricade_type = random.choice(list(CoverPlacer.BARRICADE_PATTERNS.keys()))
            dx, dy = CoverPlacer.BARRICADE_SIZES[barricade_type]

            if x + dx >= width - 1 or y + dy >= height - 1:
                continue

            points = CoverPlacer.BARRICADE_PATTERNS[barricade_type](x, y)

            if all(grid[py][px] == config.tile_empty for px, py in points):
                if barricade_type == 'car':
                    points = [p for p in points if p != (x + 1, y)]

                for px, py in points:
                    grid[py][px] = config.tile_wall
                return True

        return False

    @staticmethod
    def _add_cover_islands(grid, width, height, destruction_level):
        island_count = int(20 * destruction_level)
        for _ in range(island_count):
            CoverPlacer._try_place_cover_island(grid, width, height)

    @staticmethod
    def _try_place_cover_island(grid, width, height):
        for _ in range(100):
            x = random.randint(3, width - 4)
            y = random.randint(3, height - 4)

            if grid[y][x] != config.tile_empty:
                continue

            if not CoverPlacer._is_open_space(grid, x, y, width, height):
                continue

            island_type = random.choice(list(CoverPlacer.ISLAND_PATTERNS.keys()))
            points = CoverPlacer.ISLAND_PATTERNS[island_type](x, y)

            if any(px < 0 or py < 0 or px >= width or py >= height for px, py in points):
                continue

            if all(grid[py][px] == config.tile_empty for px, py in points):
                for px, py in points:
                    grid[py][px] = config.tile_wall
                return True

        return False

    @staticmethod
    def _is_open_space(grid, x, y, width, height):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    if grid[ny][nx] == config.tile_wall:
                        return False
        return True