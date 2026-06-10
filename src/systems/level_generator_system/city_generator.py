import random
from src.core import config


class CityGenerator:
    @staticmethod
    def generate(width, height):
        grid = [[config.tile_empty for _ in range(width)] for _ in range(height)]
        blocks_x = max(3, width // 8)
        blocks_y = max(3, height // 8)

        block_width = width // blocks_x
        block_height = height // blocks_y
        margin_x = max(1, block_width // 4)
        margin_y = max(1, block_height // 4)

        for by in range(blocks_y):
            for bx in range(blocks_x):
                if CityGenerator._should_skip_block(bx, by, blocks_x, blocks_y):
                    continue
                CityGenerator._place_buildings_in_block(
                    grid, bx, by, block_width, block_height, margin_x, margin_y
                )

        return grid

    @staticmethod
    def _should_skip_block(bx, by, blocks_x, blocks_y):
        center_bx = blocks_x // 2
        center_by = blocks_y // 2
        if abs(bx - center_bx) <= 1 and abs(by - center_by) <= 1:
            return False
        return random.random() < 0.15

    @staticmethod
    def _place_buildings_in_block(grid, bx, by, block_width, block_height, margin_x, margin_y):
        block_x_start = bx * block_width
        block_y_start = by * block_height
        block_x_end = block_x_start + block_width
        block_y_end = block_y_start + block_height

        available_width = block_width - margin_x * 2
        available_height = block_height - margin_y * 2

        if available_width < 4 or available_height < 4:
            return

        num_buildings = random.randint(1, 3)

        for _ in range(num_buildings):
            max_building_width = max(5, available_width - 2)
            max_building_height = max(5, available_height - 2)

            building_width = random.randint(5, min(7, max_building_width))
            building_height = random.randint(5, min(7, max_building_height))

            building_x = random.randint(
                block_x_start + margin_x,
                max(block_x_start + margin_x, block_x_end - margin_x - building_width)
            )
            building_y = random.randint(
                block_y_start + margin_y,
                max(block_y_start + margin_y, block_y_end - margin_y - building_height)
            )

            CityGenerator._draw_building(grid, building_x, building_y, building_width, building_height)

    @staticmethod
    def _draw_building(grid, building_x, building_y, building_width, building_height):
        for y in range(building_y, building_y + building_height):
            for x in range(building_x, building_x + building_width):
                if (y == building_y or y == building_y + building_height - 1 or
                        x == building_x or x == building_x + building_width - 1):
                    grid[y][x] = config.tile_wall
                else:
                    grid[y][x] = config.tile_empty

        if building_width >= 6 and building_height >= 6:
            CityGenerator._add_interior(grid, building_x, building_y, building_width, building_height)

    @staticmethod
    def _add_interior(grid, building_x, building_y, building_width, building_height):
        interior_x_start = building_x + 1
        interior_y_start = building_y + 1
        interior_x_end = building_x + building_width - 1
        interior_y_end = building_y + building_height - 1

        spacing = random.choice([3, 4])
        for y in range(interior_y_start + 1, interior_y_end - 1, spacing):
            for x in range(interior_x_start + 1, interior_x_end - 1, spacing):
                if random.random() < 0.7:
                    grid[y][x] = config.tile_wall

        if random.random() < 0.4:
            if random.random() < 0.5:
                wall_y = random.randint(interior_y_start + 2, interior_y_end - 2)
                for x in range(interior_x_start, interior_x_end):
                    if random.random() < 0.8:
                        grid[wall_y][x] = config.tile_wall
            else:
                wall_x = random.randint(interior_x_start + 2, interior_x_end - 2)
                for y in range(interior_y_start, interior_y_end):
                    if random.random() < 0.8:
                        grid[y][wall_x] = config.tile_wall

    @staticmethod
    def _ensure_building_exits(grid, width, height):
        for y in range(2, height - 2):
            for x in range(2, width - 2):
                if grid[y][x] == config.tile_wall:
                    if CityGenerator._is_large_building_wall(grid, x, y, width, height):
                        if random.random() < 0.3:
                            CityGenerator._create_entrance(grid, x, y, width, height)

    @staticmethod
    def _is_large_building_wall(grid, x, y, width, height):
        wall_count = sum(
            1 for dy in range(-1, 2) for dx in range(-1, 2)
            if (dy != 0 or dx != 0) and
            0 <= y + dy < height and 0 <= x + dx < width and
            grid[y + dy][x + dx] == config.tile_wall
        )
        return wall_count >= 5

    @staticmethod
    def _create_entrance(grid, x, y, width, height):
        grid[y][x] = config.tile_empty
        if random.random() < 0.5:
            if random.random() < 0.5 and x + 1 < width and grid[y][x + 1] == config.tile_wall:
                grid[y][x + 1] = config.tile_empty
            elif y + 1 < height and grid[y + 1][x] == config.tile_wall:
                grid[y + 1][x] = config.tile_empty