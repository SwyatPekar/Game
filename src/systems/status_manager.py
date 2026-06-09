from src.core import config

class GameStateManager:
    def __init__(self):
        self.state = "PLAYING"
        self.death_timer = 0.0

    def game_over(self):
        self.state = "GAME_OVER"
        self.death_timer = config.game_over_delay

    def update(self, dt: float):
        if self.state == "GAME_OVER":
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.state = "PLAYING"
                return True
        return False

    def reset(self):
        self.state = "PLAYING"
        self.death_timer = 0.0