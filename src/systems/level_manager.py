from src.systems.level_generator import LevelGenerator

class LevelManager:
    @staticmethod
    def load_level() -> tuple:
        player, walls, grid = LevelGenerator.generate()
        return player, walls, grid