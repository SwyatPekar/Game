import sys
import pygame
from src.core import config

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.window_width, config.window_height))
        icon = pygame.image.load('../assets/images/icon.png')
        pygame.display.set_caption(config.window_name)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update_display()
            self.clock.tick(config.fps)
        self.cleanup()

    def process_action(self, action):
        pass

    def update_display(self):
        self.screen.fill(config.dark_blue)
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        sys.exit()