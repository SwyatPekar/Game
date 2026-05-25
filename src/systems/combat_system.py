import pygame
from typing import List

from src.objects.weapons.projectile import Projectile
from src.combat.attack import Attack
from src.core.config import window_width, window_height


class CombatSystem:
    """
    System: Координирует боевые взаимодействия.
    Отвечает за обновление снарядов, проверку попаданий,
    применение урона и управление активными атаками.
    """

    def __init__(self):
        # Хранилище активных снарядов
        self.projectiles: List[Projectile] = []

        # Хранилище активных рукопашных атак
        # Структура: [{'attacker': Entity, 'attack': Attack, 'hit_targets': set()}]
        self.active_attacks = []

    def register_projectile(self, projectile: Projectile):
        """Добавить снаряд в систему обработки"""
        self.projectiles.append(projectile)

    def register_attack(self, attacker, attack: Attack):
        """
        Зарегистрировать рукопашную атаку.
        :param attacker: Кто атакует (Player или Enemy)
        :param attack: Объект атаки
        """
        self.active_attacks.append({
            'attacker': attacker,
            'attack': attack,
            'hit_targets': set()  # Чтобы не наносить урон одному и тому же врагу дважды за одну атаку
        })

    def update(self, dt: float, player, enemies: list, walls: list):
        """
        Главный цикл обновления боевой системы.
        """
        # 1. Обновление и проверка снарядов
        self._update_projectiles(dt, player, enemies, walls)

        # 2. Обновление и проверка рукопашных атак
        self._update_attacks(dt, player, enemies)

        # 3. Очистка неактивных объектов
        self._cleanup()

    def _update_projectiles(self, dt: float, player, enemies: list, walls: list):
        """Обновление позиции снарядов и проверка попаданий"""
        projectiles_to_remove = []

        for proj in self.projectiles:
            proj.update(dt)

            # Проверка выхода за границы экрана или столкновения со стенами
            if not (0 <= proj.x <= window_width and 0 <= proj.y <= window_height):
                projectiles_to_remove.append(proj)
                continue

            if proj.rect.collidelist([w for w in walls]) != -1:
                projectiles_to_remove.append(proj)
                continue

            # Проверка попаданий в цели
            if proj.owner_type == 'player':
                # Пуля игрока попала во врага
                for enemy in enemies:
                    if enemy.is_alive and proj.rect.colliderect(enemy.get_rect()):
                        enemy.take_damage(proj.damage)
                        projectiles_to_remove.append(proj)
                        break  # Пуля исчезает при первом попадании
            else:
                # Пуля врага попала в игрока
                if player.is_alive and not player.invincible:  # Проверка неуязвимости при перекате
                    if proj.rect.colliderect(player.get_rect()):
                        player.take_damage(proj.damage)
                        projectiles_to_remove.append(proj)

    def _update_attacks(self, dt: float, player, enemies: list):
        """Обновление таймеров атак и проверка попадания в ближнем бою"""
        attacks_to_remove = []

        for attack_data in self.active_attacks:
            attack_data['attack'].update(dt)

            if not attack_data['attack'].is_active:
                attacks_to_remove.append(attack_data)
                continue

            attacker = attack_data['attacker']
            attack_obj = attack_data['attack']
            hit_targets = attack_data['hit_targets']

            # Получаем хитбокс атаки относительно позиции атакующего
            hitbox = attack_obj.get_hitbox(
                attacker.x, attacker.y,
                attacker.width, attacker.height,
                getattr(attacker, 'facing_angle', 0)
                # У врагов может не быть facing_angle, используем 0 или вычисляем динамически
            )

            # Определяем цели (если атакует игрок -> цели враги, и наоборот)
            targets = enemies if attack_data['attacker'] == player else [player]

            for target in targets:
                if target.is_alive and target not in hit_targets:
                    # Для игрока проверяем неуязвимость
                    if target == player and target.invincible:
                        continue

                    if hitbox.colliderect(target.get_rect()):
                        target.take_damage(attack_obj.damage)
                        hit_targets.add(target)

    def _cleanup(self):
        """Удаление неактивных снарядов и завершённых атак"""
        self.projectiles = [p for p in self.projectiles if p.is_active]
        self.active_attacks = [a for a in self.active_attacks if a['attack'].is_active]