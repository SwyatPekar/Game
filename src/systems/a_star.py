import heapq
from src.core import config


class AStar:
    @staticmethod
    def find_path(grid, start, goal):
        width = len(grid[0])
        height = len(grid)

        if not (0 <= start[0] < width and 0 <= start[1] < height):
            return []
        if not (0 <= goal[0] < width and 0 <= goal[1] < height):
            return []

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return AStar._reconstruct_path(came_from, current)

            neighbors = [
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
                (current[0], current[1] + 1),
                (current[0], current[1] - 1)
            ]

            for neighbor in neighbors:
                nx, ny = neighbor
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != config.tile_wall:
                    step_cost = 1.5 if grid[ny][nx] == config.tile_rubble else 1.0

                    tentative_g_score = g_score[current] + step_cost

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        h = abs(nx - goal[0]) + abs(ny - goal[1])
                        f_score = tentative_g_score + h
                        heapq.heappush(open_set, (f_score, neighbor))

        return []

    @staticmethod
    def _reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path