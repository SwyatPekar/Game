import pygame

class InputHandler:
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def handle_events(self) -> list:
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                actions.append('shoot')
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                actions.append('kick')
        return actions

    def get_mouse_pos(self) -> tuple:
        return self.mouse_pos

    def is_key_pressed(self, key: int) -> bool:
        return bool(self.keys[key])