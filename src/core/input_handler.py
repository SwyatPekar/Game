import pygame


class InputHandler:
    """
    Controller: Обработка пользовательского ввода.
    Преобразует события Pygame в игровые действия (Action).
    """

    def __init__(self, screen):
        self.screen = screen

    def handle_events(self) -> str | None:
        """
        Обрабатывает очередь событий.
        Возвращает строку действия ('shoot', 'kick', 'quit') или None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            # Стрельба по нажатию левой кнопки мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return 'shoot'

            # Пинок по нажатию пробела
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 'kick'

        return None