import pygame
from src.core import config

class WorldRenderer:
    def __init__(self, screen: pygame.Surface, player_renderer, health_bar_renderer, projectile_renderer):
        self.screen = screen
        self.game_info = Game_Info

        self.player_renderer = player_renderer
        self.health_bar_renderer = health_bar_renderer
        self.projectile_renderer = projectile_renderer

    def render(self, walls, enemies, projectiles, player, wave_manager):
        self.screen.fill(config.dark_blue)

        for wall in walls:
            pygame.draw.rect(self.screen, config.wall_color, wall)

        for enemy in enemies:
            if enemy.is_alive:
                enemy.draw(self.screen)

        for projectile in projectiles:
            self.projectile_renderer.render(self.screen, projectile)

        if player.is_alive:
            player.draw(self.screen, self.player_renderer, self.health_bar_renderer)

        self.game_info.render(self.screen, wave_manager)

        pygame.display.flip()


class Game_Info:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 20)

    def render(self, screen: pygame.Surface, wave_manager):
        info = wave_manager.get_wave_info()
        score = info.get('score', 0)
        text = f"Wave: {info['wave']} | {info['state']} | Score: {score}"

        rendered_text = self.font.render(text, True, config.white)
        screen.blit(rendered_text, (10, 10))