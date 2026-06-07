from src.objects.player import Player
from src.tests.test_walls import create_test_walls
from src.tests.debug_config import test_player_spawn_x, test_player_spawn_y

class LevelManager:
    @staticmethod
    def load_level() -> tuple[Player, list]:
        player = Player(test_player_spawn_x, test_player_spawn_y)
        walls = create_test_walls()
        return player, walls