# Mass effect: They Will Not Break Us

# Окно программы
window_name = "Mass effect: They Will Not Break Us"
window_width = 1200
window_height = 800
fps = 60

# Цвета
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 25)
light_green = (0, 170, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
orange = (255, 140, 0)
purple = (128, 0, 128)
dark_purple = (75, 0, 130)
brown = (139, 69, 19)
dark_green = (0, 100, 0)
cyan = (0, 191, 255)
gray = (128, 128, 128)
wall_color = (100, 100, 100)

# Игрок
player_width = 32
player_height = 32
player_speed = 200
player_max_health = 100
player_damage = 10
bullet_speed = 600

# Перекат
player_roll_speed = 400
player_roll_duration = 0.2
player_roll_cooldown = 1.0
player_invincible_frames = True

# Ближний бой
player_kick_range = 40
player_kick_damage = 15

# Враги (базовые статы вынесены сюда для удобства расширения)
enemy_base_width = 32
enemy_base_height = 32
enemy_base_speed = 100
enemy_base_health = 50
enemy_base_damage = 10
enemy_base_attack_range = 40
enemy_detection_range = 400
enemy_attack_cooldown = 1.0
enemy_patrol_timer = 2.0
health_bar_height_enemy = 4
health_bar_offset_y_enemy = 8

# UI
health_bar_width = 40
health_bar_height = 5
health_bar_offset_y = 10

# Снаряды
projectile_radius = 4

# Отладка
debug_mode = True
show_collision_boxes = False
show_ai_states = False

# Индикатор направления
direction_line_color = yellow
direction_line_length = 25

# Волны
wave_rest_duration = 10.0
wave_spawn_interval = 1.5
initial_enemies_count = 5
enemies_increment = 2