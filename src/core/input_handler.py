import pygame
from src.core import config

class InputHandler:
    def __init__(self, screen):
        self.screen = screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
        return None