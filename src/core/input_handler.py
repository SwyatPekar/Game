import pygame


class InputHandler:

    def __init__(self, screen):
        self.screen = screen

    def handle_events(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return 'shoot'

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 'kick'

        return None