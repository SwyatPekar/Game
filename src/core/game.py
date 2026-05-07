import sys
import pygame
from src.core import config

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.window_width, config.window_height))
        pygame.display.set_caption(config.window_name)
        self.clock = pygame.time.Clock()
        self.running = True


    def run(self):
        pass

    def process_action(self, action):
        pass

    def update_display(self):
        pass

    def cleanup(self):
        pygame.quit()
        sys.exit()