import pygame
import math


class Attack:
    """
    Model: Абстракция атаки (преимущественно ближний бой).
    Содержит параметры атаки: урон, радиус, длительность.
    НЕ содержит отрисовку или логику применения урона.
    """

    def __init__(self, damage: int, range: float, duration: float = 0.1, is_melee: bool = True):
        """
        :param damage: Урон атаки
        :param range: Дальность атаки (радиус в пикселях)
        :param duration: Длительность активности атаки (секунды)
        :param is_melee: Флаг ближнего боя (для будущих дальнобойных атак)
        """
        self.damage = damage
        self.range = range
        self.duration = duration
        self.is_melee = is_melee
        self.is_active = True
        self.timer = duration  # Обратный отсчёт для авто-деактивации

    def update(self, dt: float):
        """
        Обновление таймера атаки.
        Вызывается каждый кадр, пока атака активна.
        """
        self.timer -= dt
        if self.timer <= 0:
            self.is_active = False

    def get_hitbox(self, attacker_x: float, attacker_y: float, attacker_width: int,
                   attacker_height: int, facing_angle: float) -> pygame.Rect:
        """
        Вычисляет хитбокс атаки относительно позиции атакующего.

        :param attacker_x: Позиция X атакующего
        :param attacker_y: Позиция Y атакующего
        :param attacker_width: Ширина атакующего
        :param attacker_height: Высота атакующего
        :param facing_angle: Угол направления атакующего (в радианах)
        :return: pygame.Rect - хитбокс атаки
        """
        # Центр атакующего
        center_x = attacker_x + attacker_width / 2
        center_y = attacker_y + attacker_height / 2

        # Смещение хитбокса в направлении атаки
        offset_x = math.cos(facing_angle) * (self.range / 2)
        offset_y = math.sin(facing_angle) * (self.range / 2)

        # Позиция хитбокса (квадрат перед атакующим)
        hitbox_x = center_x + offset_x - self.range / 2
        hitbox_y = center_y + offset_y - self.range / 2

        return pygame.Rect(hitbox_x, hitbox_y, self.range, self.range)