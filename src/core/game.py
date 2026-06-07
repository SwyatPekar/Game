import sys
import pygame
from src.core import config
from src.core.input_handler import InputHandler
from src.objects.player import Player
from src.rendering.entities.player_render import PlayerRenderer
from src.rendering.effects.health_bar_render import HealthBarRenderer
from src.rendering.effects.projectile_render import ProjectileRenderer
from src.tests.test_walls import create_test_walls
from src.tests.debug_config import test_player_spawn_x, test_player_spawn_y
from src.systems.combat_system import CombatSystem
from src.systems.wave_manager import WaveManager


class GameEngine:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.window_width, config.window_height))
        icon = pygame.image.load('../assets/images/icon.png')
        pygame.display.set_caption(config.window_name)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True

        self.input_handler = InputHandler()
        self.player_renderer = PlayerRenderer()
        self.health_bar_renderer = HealthBarRenderer()
        self.projectile_renderer = ProjectileRenderer()

        self.player = self._create_player()
        self.walls = create_test_walls()

        self.combat_system = CombatSystem()

        self.wave_manager = WaveManager(config.window_width, config.window_height)

    def run(self):
        while self.running:
            dt = self.clock.tick(config.fps) / 1000.0

            action = self.input_handler.handle_events()

            self._update(dt)

            self._render()

            self._process_action(action)

            if not self.player.is_alive:
                print(f"Игрок погиб. Счёт: {self.wave_manager.get_wave_info()['score']}")
                pygame.time.wait(1500)
                self.__init__()

    def _create_player(self) -> Player:
        return Player(test_player_spawn_x, test_player_spawn_y)

    def _update(self, dt: float):

        if self.wave_manager.state == "WAITING":
            self.wave_manager.start_game()

        self.wave_manager.update(dt, self.walls)

        active_enemies = self.wave_manager.get_enemies()

        if self.player.is_alive:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.player.update(dt, keys, mouse_pos, self.walls)

        for enemy in active_enemies:
            if enemy.is_alive:
                enemy.update(dt, self.player, self.walls)

        self.combat_system.update(dt, self.player, active_enemies, self.walls)

    def _render(self):
        self.screen.fill(config.dark_blue)

        for wall in self.walls:
            pygame.draw.rect(self.screen, config.wall_color, wall)

        for enemy in self.wave_manager.get_enemies():
            enemy.draw(self.screen)

        for projectile in self.combat_system.projectiles:
            self.projectile_renderer.render(self.screen, projectile)

        if self.player.is_alive:
            self.player.draw(
                self.screen,
                self.player_renderer,
                self.health_bar_renderer
            )

        self._render_hud()

        pygame.display.flip()

    def _render_hud(self):
        font = pygame.font.SysFont("Arial", 20)
        info = self.wave_manager.get_wave_info()

        text_wave = font.render(f"Wave: {info['wave']} | {info['state']}", True, config.white)
        self.screen.blit(text_wave, (10, 10))

    def _process_action(self, action):
        if action == 'quit':
            self.running = False

        elif action == 'shoot' and self.player.is_alive:
            projectile = self.player.shoot()
            self.combat_system.register_projectile(projectile)

        elif action == 'kick' and self.player.is_alive:
            attack = self.player.kick()
            self.combat_system.register_attack(self.player, attack)

    def cleanup(self):
        pygame.quit()
        sys.exit()


class game_info:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 20)

    def render(self, screen: pygame.Surface, wave_manager):
        info = wave_manager.get_wave_info()
        score = info.get('score', 0)
        text = f"Wave: {info['wave']} | {info['state']} | Score: {score}"

        rendered_text = self.font.render(text, True, config.white)
        screen.blit(rendered_text, (10, 10))