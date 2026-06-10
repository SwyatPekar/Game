import pygame
from src.objects.weapons.projectile import Projectile
from src.core import config


class ProjectileRenderer:
    def __init__(self):
        self.colors = {
            'player': config.yellow,
            'enemy': config.red
        }

    def render(self, screen: pygame.Surface, projectile: Projectile):
        color = self.colors.get(projectile.owner_type, config.white)

        pygame.draw.circle(screen, color, (int(projectile.x), int(projectile.y)),projectile.radius)

        pygame.draw.circle(screen, config.black,(int(projectile.x), int(projectile.y)), projectile.radius, 1)