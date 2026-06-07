import sys
import pygame
from src.core import config
from src.core.input_handler import InputHandler
from src.systems.status_manager import GameStateManager
from src.systems.level_manager import LevelManager
from src.rendering.render import WorldRenderer
from src.rendering.entities.player_render import PlayerRenderer
from src.rendering.effects.health_bar_render import HealthBarRenderer
from src.rendering.effects.projectile_render import ProjectileRenderer
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
        self.state_manager = GameStateManager()
        self.level_manager = LevelManager()

        self.player_renderer = PlayerRenderer()
        self.health_bar_renderer = HealthBarRenderer()
        self.projectile_renderer = ProjectileRenderer()

        self.renderers = {
            'player': self.player_renderer,
            'health_bar': self.health_bar_renderer,
            'projectile': self.projectile_renderer
        }

        self.renderer = WorldRenderer(
            self.screen,
            self.renderers
        )

        self.combat_system = CombatSystem(config.window_width, config.window_height)
        self.wave_manager = WaveManager(config.window_width, config.window_height)

        self.reset_game()

    def reset_game(self):
        self.player, self.walls, self.grid = self.level_manager.load_level()
        self.wave_manager.reset()
        self.combat_system.reset()
        self.state_manager.reset()

    def run(self):
        while self.running:
            dt = self.clock.tick(config.fps) / 1000.0

            self.input_handler.update()

            action = self.input_handler.handle_events()
            if action == 'quit':
                self.running = False
                break

            if self.state_manager.state == "PLAYING":
                self._update(dt)
                self._process_action(action)

                if not self.player.is_alive:
                    print(f"Игрок погиб. Счёт: {self.wave_manager.get_wave_info().get('score', 0)}")
                    self.state_manager.game_over()

            elif self.state_manager.state == "GAME_OVER":
                if self.state_manager.update(dt):
                    self.reset_game()

            self.renderer.render(
                self.walls,
                self.wave_manager.get_enemies(),
                self.combat_system.projectiles,
                self.player,
                self.wave_manager,
                self.renderers
            )

        self.cleanup()

    def _update(self, dt: float):
        if self.wave_manager.state == "WAITING":
            self.wave_manager.start_game()

        self.wave_manager.update(dt, self.walls, self.grid)
        active_enemies = self.wave_manager.get_enemies()

        if self.player.is_alive:
            self.player.update(
                dt,
                self.input_handler.keys,
                self.input_handler.mouse_pos,
                self.walls)

        for enemy in active_enemies:
            if enemy.is_alive:
                enemy.update(dt, self.player, self.walls, self.grid)

                if enemy.current_attack:
                    self.combat_system.register_attack(enemy, enemy.current_attack)

        self.combat_system.update(dt, self.player, active_enemies, self.walls)

    def _process_action(self, action):
        if action == 'shoot' and self.player.is_alive:
            projectile = self.player.shoot()
            if projectile:
                self.combat_system.register_projectile(projectile)

        elif action == 'kick' and self.player.is_alive:
            attack = self.player.kick()
            if attack:
                self.combat_system.register_attack(self.player, attack)

    def cleanup(self):
        pygame.quit()
        sys.exit()