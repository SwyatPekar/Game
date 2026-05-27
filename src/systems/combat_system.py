import pygame
from typing import List

from src.objects.weapons.projectile import Projectile
from src.combat.attack import Attack
from src.core.config import window_width, window_height


class CombatSystem:
    def __init__(self):
        self.projectiles: List[Projectile] = []
        self.active_attacks = []

    def register_projectile(self, projectile: Projectile):
        self.projectiles.append(projectile)

    def register_attack(self, attacker, attack: Attack):
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
        projectiles_to_remove = []

        for proj in self.projectiles:
            proj.update(dt)

            if not (0 <= proj.x <= window_width and 0 <= proj.y <= window_height):
                projectiles_to_remove.append(proj)
                continue

            if proj.rect.collidelist([w for w in walls]) != -1:
                projectiles_to_remove.append(proj)
                continue

            if proj.owner_type == 'player':
                for enemy in enemies:
                    if enemy.is_alive and proj.rect.colliderect(enemy.get_rect()):
                        enemy.take_damage(proj.damage)
                        projectiles_to_remove.append(proj)
                        break
            else:
                if player.is_alive and not player.invincible:
                    if proj.rect.colliderect(player.get_rect()):
                        player.take_damage(proj.damage)
                        projectiles_to_remove.append(proj)

    def _update_attacks(self, dt: float, player, enemies: list):
        attacks_to_remove = []

        for attack_data in self.active_attacks:
            attack_data['attack'].update(dt)

            if not attack_data['attack'].is_active:
                attacks_to_remove.append(attack_data)
                continue

            attacker = attack_data['attacker']
            attack_obj = attack_data['attack']
            hit_targets = attack_data['hit_targets']

            hitbox = attack_obj.get_hitbox(
                attacker.x, attacker.y,
                attacker.width, attacker.height,
                getattr(attacker, 'facing_angle', 0)
            )

            targets = enemies if attack_data['attacker'] == player else [player]

            for target in targets:
                if target.is_alive and target not in hit_targets:
                    if target == player and target.invincible:
                        continue

                    if hitbox.colliderect(target.get_rect()):
                        target.take_damage(attack_obj.damage)
                        hit_targets.add(target)

    def _cleanup(self):
        self.projectiles = [p for p in self.projectiles if p.is_active]
        self.active_attacks = [a for a in self.active_attacks if a['attack'].is_active]