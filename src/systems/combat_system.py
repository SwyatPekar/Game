import pygame
from typing import List

from src.objects.weapons.projectile import Projectile
from src.combat.attack import Attack
from src.core.config import window_width, window_height


class CombatSystem:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.projectiles: List = []
        self.active_attacks = []

    def register_projectile(self, projectile):
        self.projectiles.append(projectile)

    def register_attack(self, attacker, attack):
        self.active_attacks.append({
            'attacker': attacker,
            'attack': attack,
            'hit_targets': set()
        })

    def update(self, dt: float, player, enemies: list, walls: list):
        self._update_projectiles(dt, player, enemies, walls)
        self._update_attacks(dt, player, enemies)
        self._cleanup()

    def _update_projectiles(self, dt: float, player, enemies: list, walls: list):
        for proj in self.projectiles:
            if not proj.is_active:
                continue

            proj.update(dt)

            if not (0 <= proj.x <= self.window_width and 0 <= proj.y <= self.window_height):
                proj.is_active = False
                continue

            if walls and proj.rect.collidelist(walls) != -1:
                proj.is_active = False
                continue

            if proj.owner_type == 'player':
                for enemy in enemies:
                    if enemy.is_alive and proj.rect.colliderect(enemy.get_rect()):
                        enemy.take_damage(proj.damage)
                        proj.is_active = False
                        break
            else:
                if player.is_alive and not getattr(player, 'invincible', False):
                    if proj.rect.colliderect(player.get_rect()):
                        player.take_damage(proj.damage)
                        proj.is_active = False

    def _update_attacks(self, dt: float, player, enemies: list):
        for attack_data in self.active_attacks:
            attack = attack_data['attack']
            if not attack.is_active:
                continue

            attack.update(dt)

            attacker = attack_data['attacker']
            hit_targets = attack_data['hit_targets']

            hitbox = attack.get_hitbox(
                attacker.x, attacker.y,
                attacker.width, attacker.height,
                getattr(attacker, 'facing_angle', 0)
            )

            targets = enemies if attacker == player else [player]

            for target in targets:
                if target.is_alive and target not in hit_targets:
                    if target == player and getattr(target, 'invincible', False):
                        continue

                    if hitbox.colliderect(target.get_rect()):
                        target.take_damage(attack.damage)
                        hit_targets.add(target)

    def _cleanup(self):
        self.projectiles = [p for p in self.projectiles if p.is_active]
        self.active_attacks = [a for a in self.active_attacks if a['attack'].is_active]