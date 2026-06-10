import pygame
from src.core import config
from src.rendering.entities.entity_render import EntityRenderer

class EnemyRenderer:
    def __init__(self):
        self.base_renderer = EntityRenderer()

    def render(self, screen: pygame.Surface, enemy, renderers: dict):
        self.base_renderer.render(screen, enemy)

        if enemy.health < enemy.max_health and renderers and 'health_bar' in renderers:
            renderers['health_bar'].render(screen, enemy, is_enemy=True)

        if config.debug_mode:
            center_x = int(enemy.x + enemy.width / 2)
            center_y = int(enemy.y + enemy.height / 2)

            if config.show_ai_states:
                font = pygame.font.SysFont("Arial", 12)
                text = font.render(enemy.state, True, config.white)
                screen.blit(text, (enemy.x, enemy.y - 20))
                pygame.draw.circle(screen, config.cyan, (center_x, center_y), int(enemy.detection_range), 1)

            if config.show_collision_boxes:
                pygame.draw.circle(screen, config.yellow, (center_x, center_y), int(enemy.attack_range), 1)
                pygame.draw.rect(screen, config.red, enemy.get_rect(), 1)