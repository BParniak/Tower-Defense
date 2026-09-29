import pygame
import sys
import os
import random
import time

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 4096)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "Pixel Art")

pygame.mixer.music.load(os.path.join(BASE_DIR, "1332458_Raze-The-Void.mp3"))
pygame.mixer.music.play()

WIDTH, HEIGHT = 1500, 800
TILE_COLS = 11
TILE_ROWS = 11
TILE_WIDTH = WIDTH // TILE_COLS
TILE_HEIGHT = HEIGHT // TILE_ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

tower_filenames = [
    "Base Tower.png",
    "Commander Base base lv.png",
    "Demolition Expert base lv.png",
    "Gunner base lv.png",
    "Minigunner base lv.png",
    "Sniper base lv.png",
    "Shotgunner base lv.png"
]

tower_costs = {
    "BaseTower": 2500,
    "BaseCommanderbase": 900,
    "BaseDemolitionExpert": 1000,
    "BaseGunner": 200,
    "BaseMinigunner": 5000,
    "BaseMoneyFarm": 200,
    "BaseSniper": 1200,
    "BaseShotgunner": 1200
}

commander_boost_active = False

class BaseTower:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 0
        self.fire_rate = 100 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.slowdown_effect = 0.5 # 20% slow effect
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Base Tower.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def apply_slowdown(self, enemies):
        for enemy in enemies:
            if enemy.alive and self.in_range(enemy):
                # Only apply the slowdown once
                if not hasattr(enemy, 'slowed_by_tower') or not enemy.slowed_by_tower:
                    original_speed = enemy.speed
                    enemy.speed *= (1 - self.slowdown_effect) # Slow the enemy by 20%
                    enemy.slowed_by_tower = True # Mark this enemy as slowed by this tower
                    print(f"Enemy {enemy.kind} slowed by 20%. New speed: {enemy.speed}")

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            self.apply_slowdown(enemies) # Apply the slowdown effect to all enemies in range
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    # Apply damage to enemy
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of Tower at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

class BaseCommanderbase:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 12
        self.fire_rate = 2.8 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Commander Base base lv.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        # Get the enemy's position (Vector2)
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of Commander Base at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

class BaseDemolitionExpert:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 8
        self.fire_rate = 10 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Demolition expert base lv.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        # Get the enemy's position (Vector2)
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of Demolition expert at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

class BaseGunner:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 4
        self.fire_rate = 5 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Gunner base lv.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        # Get the enemy's position (Vector2)
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of gunner at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

class BaseMinigunner:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 2
        self.fire_rate = 1 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Minigunner base lv.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        # Get the enemy's position (Vector2)
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of Minigunner at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

class BaseSniper:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 150
        self.fire_rate = 30 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Sniper Base lv.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        # Get the enemy's position (Vector2)
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of Sniper at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.tile_size * self.range

class BaseShotgunner:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.range = 10000
        self.damage = 85
        self.fire_rate = 10 # seconds per shot
        self.time_since_last_shot = 0 # <-- track time using dt
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "Shotgunner Base lv.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def in_range(self, enemy):
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2))
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2))
        return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

    def update(self, enemies, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.fire_rate:
            for enemy in enemies:
                if enemy.alive and self.in_range(enemy):
                    print(f"{enemy.kind} at {enemy.pos} taking {self.damage} damage! HP before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    print(f" → HP after: {enemy.health}")
                    self.time_since_last_shot = 0
                    break

    def in_range(self, enemy):
        # Get the enemy's position (Vector2)
        dx = abs(enemy.pos.x - (self.x * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        dy = abs(enemy.pos.y - (self.y * self.tile_size + self.tile_size / 2)) # Adjusted for center position
        if dx <= self.range * self.tile_size and dy <= self.range * self.tile_size:
            print(f"Enemy {enemy.kind} is in range of Shotgunner at ({self.x}, {self.y})")
            return dx <= self.range * self.tile_size and dy <= self.range * self.tile_size

tower_classes = [
    BaseTower, BaseCommanderbase, BaseDemolitionExpert,
    BaseGunner, BaseMinigunner, BaseSniper, BaseShotgunner
]

tower_objects = []

tower_sizes = [
    (80, 80), # Base Tower original size (80, 80)
    (100, 60), # Commander original size (100, 60)
    (35, 61), # Demolition Expert original size (117, 202)
    (33, 59), # Gunner original size (47, 84)
    (60, 60), # Minigunner original size (60, 60)
    (64, 96), # Sniper original size (80, 120)
    (82, 59) # Shotgunner original size (63, 45)
]

tower_images = []
for name, size in zip(tower_filenames, tower_sizes):
    asset_path = os.path.join(ASSET_DIR, name)
    try:
        img = pygame.image.load(asset_path).convert_alpha()
        img = pygame.transform.scale(img, size)
        tower_images.append(img)
    except Exception:
        print(f"Could not load {asset_path}")
        tower_images.append(None)

invalid_tiles = {
    (0, 3), (1, 1), (1, 2), (1, 3), (2, 1), (2, 5), (2, 6), (2, 7), (2, 8),
    (3, 1), (3, 5), (3, 8), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 8),
    (5, 8), (6, 8), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8),
    (8, 1), (8, 6), (8, 8), (9, 1), (9, 2), (9, 3), (9, 6), (9, 7), (9, 8),
    (10, 3), (11, 4)
}

invalid_tiles.update({(col, 10) for col in range(TILE_COLS)})

def get_tile_under_mouse():
    mx, my = pygame.mouse.get_pos()
    col = mx // TILE_WIDTH
    row = my // TILE_HEIGHT
    return col, row

def get_tile_center(col, row):
    return col * TILE_WIDTH + TILE_WIDTH // 2, row * TILE_HEIGHT + TILE_HEIGHT // 2

def is_tile_occupied(col, row):
    for tower in placed_towers:
        if tower[0] == col and tower[1] == row:
            return True
    return False

tower_selectors = []
for i, img in enumerate(tower_images):
    w, h = tower_sizes[i]
    x = i * TILE_WIDTH + TILE_WIDTH // 2
    y = 10 * TILE_HEIGHT + TILE_HEIGHT // 2
    rect = pygame.Rect(x - w//2, y - h//2, w, h)
    tower_selectors.append(rect)

placed_towers = []
dragging_tower = None

standard_path = [
    (1480, 210), (1220, 210), (1220, 60), (950, 60),
    (950, 420), (1250, 420), (1250, 550), (300, 550),
    (300, 325), (550, 325), (550, 60), (175, 60),
    (175, 200), (0, 200)
]

miniboss_path = [
    (1480, 190), (1220, 190), (1220, 40), (950, 40), (950, 400), (1250, 400),
    (1250, 530), (300, 530), (300, 305), (550, 305), (550, 40), (175, 40),
    (175, 180), (0, 180)
]

bigtank_path = [
    (1480, 165), (1220, 165), (1220, 15), (950, 15), (950, 375), (1250, 375),
    (1250, 505), (300, 505), (300, 280), (550, 280), (550, 15), (175, 15),
    (175, 155), (0, 155)
]

guardian_path = [
    (1480, 100), (1220, 100), (1220, -50), (950, -50), (950, 315), (1250, 315),
    (1250, 445), (300, 445), (300, 215), (550, 215), (550, -50), (175, -50),
    (175, 90), (0, 90)
]

boss_path = [
    (1480, 0), (1180, 0), (1180, -150), (910, -150), (910, 215), (1210, 215),
    (1210, 345), (260, 345), (260, 115), (510, 115), (510, -150), (135, -150),
    (135, -10), (-40, -10)
]

map_img = pygame.image.load(os.path.join(ASSET_DIR, "Map.png")).convert_alpha()
map_img = pygame.transform.scale(map_img, (1500, 800))

def resolve_asset_folder(base_path, folder_name):
    folder_path = os.path.join(base_path, folder_name)
    if os.path.isdir(folder_path):
        return folder_path

    for entry in sorted(os.listdir(base_path)):
        if entry.lower() == folder_name.lower():
            return os.path.join(base_path, entry)

    return folder_path


def load_animation_frames(folder_path, scale=0.3):
    if not os.path.isdir(folder_path):
        print(f"Warning: animation folder not found: {folder_path}")
        return []

    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.png'):
            img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            img = pygame.transform.scale(img, (
                int(img.get_width() * scale), int(img.get_height() * scale)
            ))
            frames.append(img)
    return frames

ASSETS_PATH = os.path.join(ASSET_DIR, 'enemy_frames')

enemy_scales = {
    'zombie': 0.3, 'speedy': 0.3, 'heavy': 0.3, 'hidden': 0.3, 'flying': 0.33,
    'miniboss': 0.375, 'necromancer': 0.3, 'bigtank': 0.45, 'guardian': 0.35, 'boss': 0.3
}

enemy_animations = {
    name: load_animation_frames(resolve_asset_folder(ASSETS_PATH, name), scale=scale)
    for name, scale in enemy_scales.items()
}

necromancer_summon_frames = load_animation_frames(resolve_asset_folder(ASSETS_PATH, 'sum'), scale=0.3)
boss_attack_frames = load_animation_frames(resolve_asset_folder(ASSETS_PATH, 'boss attack'), scale=0.3)
boss_stomp_frames = load_animation_frames(resolve_asset_folder(ASSETS_PATH, 'boss stomp'), scale=0.3)

enemy_stats = {
    'zombie': {'speed': 100}, 'speedy': {'speed': 125}, 'heavy': {'speed': 75},
    'hidden': {'speed': 110}, 'flying': {'speed': 100}, 'miniboss': {'speed': 85},
    'necromancer': {'speed': 40}, 'bigtank': {'speed': 50}, 'guardian': {'speed': 50},
    'boss': {'speed': 25},
}

class Enemy:
    def __init__(self, kind, path, speed, frames):
        self.kind = kind
        self.path = path
        self.speed = speed
        self.frames = frames
        self.default_frames = frames
        self.pos = pygame.math.Vector2(path[0])
        self.target_index = 1
        self.alive = True
        enemy_health_values = {
            'zombie': 10, 'speedy': 8, 'heavy': 35, 'hidden': 15, 'flying': 15,
            'miniboss': 100, 'necromancer': 40, 'bigtank': 750, 'guardian': 1000,
            'boss': 50000
        }
        self.max_health = enemy_health_values.get(kind, 1)
        self.health = self.max_health
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.summon_timer = 0
        self.summon_cooldown = 8 if kind == 'necromancer' else 0
        self.attack_timer = 0
        self.attack_cooldown = 10 if kind == 'boss' else 0
        self.state = "walk"
        self.state_timer = 0

    def take_damage(self, damage):
        self.health -= damage
        print(f"[{self.kind}] Took {damage} damage → health: {self.health}")
        if self.health <= 0:
            print(f"[{self.kind}] has died.")
            self.alive = False

    def update(self, dt):
        if self.target_index >= len(self.path):
            self.alive = False
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        if self.kind == 'necromancer':
            if self.state == "summoning":
                self.state_timer -= dt
                if self.state_timer <= 0:
                    self.state = "walk"
                    self.frames = self.default_frames
                    self.frame_index = 0
                return

        if self.kind == 'boss':
            if self.state in ["attacking", "stomping"]:
                self.state_timer -= dt
                if self.state_timer <= 0:
                    self.state = "walk"
                    self.frames = self.default_frames
                    self.frame_index = 0
                return

        target = pygame.math.Vector2(self.path[self.target_index])
        direction = target - self.pos
        distance = direction.length()
        if distance < self.speed * dt:
            self.pos = target
            self.target_index += 1
        else:
            direction.normalize_ip()
            self.pos += direction * self.speed * dt

        if self.kind == 'necromancer':
            self.summon_timer += dt
            if self.summon_timer >= self.summon_cooldown:
                self.summon_timer = 0
                self.state = "summoning"
                self.state_timer = 1.2
                self.frames = necromancer_summon_frames
                self.frame_index = 0
                summon_kinds = ['zombie', 'speedy', 'heavy', 'hidden']
                for _ in range(random.randint(1, 10)):
                    kind = random.choice(summon_kinds)
                    speed = enemy_stats[kind]['speed']
                    frames = enemy_animations[kind]
                    enemies.append(Enemy(kind, standard_path, speed, frames))

        if self.kind == 'boss':
            self.attack_timer += dt
            if self.attack_timer >= self.attack_cooldown:
                self.attack_timer = 0
                self.state = random.choice(["attacking", "stomping"])
                self.state_timer = 1.5
                self.frames = boss_attack_frames if self.state == "attacking" else boss_stomp_frames
                self.frame_index = 0
                summon_kinds = ['miniboss', 'bigtank', 'necromancer', 'guardian']
                for _ in range(random.randint(1, 10)):
                    kind = random.choice(summon_kinds)
                    speed = enemy_stats[kind]['speed']
                    frames = enemy_animations[kind]
                    if kind == 'miniboss':
                        path = miniboss_path
                    elif kind == 'bigtank':
                        path = bigtank_path
                    elif kind == 'guardian':
                        path = guardian_path
                    else:
                        path = standard_path
                    enemies.append(Enemy(kind, path, speed, frames))

    def draw(self, surface):
        frame = self.frames[self.frame_index]
        x, y = int(self.pos.x), int(self.pos.y)
        flip = not (
            (self.kind == 'miniboss' and ((x == 950 and 40 <= y <= 400) or
            (950 <= x <= 1250 and y == 400) or (300 <= x <= 550 and y == 305))) or
            (self.kind == 'bigtank' and ((x == 950 and 15 <= y <= 375) or
            (950 <= x <= 1250 and y == 375) or (300 <= x <= 550 and y == 280))) or
            (self.kind == 'guardian' and ((x == 950 and -50 <= y <= 315)
            or (950 <= x <= 1250 and y == 315) or (300 <= x <= 550 and y == 215))) or
            (self.kind == 'boss' and ((x == 910 and -150 <= y <= 215) or
            (910 <= x <= 1210 and y == 215) or (260 <= x <= 510 and y == 115))) or
            ((x == 950 and 60 <= y <= 420) or (950 <= x <= 1250 and y == 420) or
            (300 <= x <= 550 and y == 325))
        )
        flipped_frame = pygame.transform.flip(frame, flip, False)
        surface.blit(flipped_frame, (x, y))

def create_wave_enemies(wave_list):
    result = []
    for kind in wave_list:
        speed = enemy_stats[kind]['speed']
        frames = enemy_animations[kind]
        path_used = {
            'miniboss': miniboss_path,
            'bigtank': bigtank_path,
            'guardian': guardian_path,
            'boss': boss_path,
        }.get(kind, standard_path)
        result.append((kind, path_used, speed, frames))
    return result

waves = [
    ['zombie'] * 20,
    ['zombie'] * 20 + ['speedy'] * 10 + ['heavy'] * 5,
    ['zombie'] * 30 + ['speedy'] * 15 + ['heavy'] * 5 + ['hidden'],
    ['hidden'] * 20 + ['flying'] * 10,
    [random.choice(['zombie', 'speedy', 'heavy', 'hidden', 'flying']) for _ in range(50)] + ['miniboss'] * 2,
    [random.choice(['zombie', 'speedy', 'heavy', 'hidden', 'flying']) for _ in range(100)] + ['miniboss'] * 4,
    ['miniboss'] * 10 + ['bigtank'] * 2 + ['necromancer'],
    ['miniboss'] * 15 + ['bigtank'] * 4 + ['necromancer'] * 2,
    ['miniboss'] * 20 + ['bigtank'] * 6 + ['guardian'] * 2 + ['necromancer'] * 3,
    ['miniboss'] * 20 + ['bigtank'] * 5 + ['guardian'] * 2 + ['boss']
]

current_wave = 0
wave_timer = 0
wave_duration = 40
wave_started = False
enemies = []
spawn_queue = []
spawn_delay = 0
player_cash = 100000000000000000 # Starting cash
enemy_cash_values = {
    'zombie': 5,
    'speedy': 4,
    'heavy': 25,
    'hidden': 10,
    'flying': 10,
    'miniboss': 100,
    'bigtank': 750,
    'guardian': 3000,
    'boss': 10000
}

font = pygame.font.SysFont(None, 36)

while True:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if event.button == 3: # Right click cancels dragging
                dragging_tower = None
            elif dragging_tower is None:
                for idx, rect in enumerate(tower_selectors):
                    if rect.collidepoint(mx, my):
                        cls = tower_classes[idx] # your list of tower classes
                        cost = tower_costs[cls.__name__] # lookup by class name
                        if player_cash >= cost:
                            dragging_tower = idx
                        else:
                            print(f"Not enough cash (${player_cash}) for {cls.__name__} (${cost})")
                        break
            else:
                # Try to place the tower on the tile under mouse
                col, row = get_tile_under_mouse()
                if (col, row) not in invalid_tiles and not is_tile_occupied(col, row):
                    placed_towers.append((col, row, dragging_tower))
                    # List of tower classes, indexed to match selectors
                    tower_classes = [
                        BaseTower,
                        BaseCommanderbase,
                        BaseDemolitionExpert,
                        BaseGunner,
                        BaseMinigunner,
                        BaseSniper,
                        BaseShotgunner
                    ]
                    # Instantiate the selected tower if it's a valid index
                    if 0 <= dragging_tower < len(tower_classes):
                        tower_class = tower_classes[dragging_tower]
                        tower = tower_class(col, row, TILE_WIDTH)
                        tower_objects.append(tower)

                    name = tower_classes[dragging_tower].__name__
                    cost = tower_costs[name]
                    player_cash -= cost
                    placed_towers.append((col, row, dragging_tower))
                    tower = tower_classes[dragging_tower](col, row, TILE_WIDTH)
                    tower_objects.append(tower)
                    dragging_tower = None

    screen.blit(map_img, (0, 0))
    for col in range(TILE_COLS):
        for row in range(TILE_ROWS):
            color = (0, 255, 0) if (col, row) not in invalid_tiles else (255, 0, 0)
            rect = pygame.Rect(col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
            pygame.draw.rect(screen, color, rect, 1)

    for idx, rect in enumerate(tower_selectors):
        if tower_images[idx]:
            screen.blit(tower_images[idx], rect.topleft)
        else:
            pygame.draw.rect(screen, (0, 0, 255), rect)

    if dragging_tower is not None:
        mx, my = pygame.mouse.get_pos()
        if tower_images[dragging_tower]:
            screen.blit(tower_images[dragging_tower], (mx - 30, my - 30))
        else:
            pygame.draw.circle(screen, (0, 0, 255), (mx, my), 30)

    for col, row, idx in placed_towers:
        cx, cy = get_tile_center(col, row)
        if tower_images[idx]:
            tower_img = tower_images[idx]
            tower_rect = tower_img.get_rect(center=(cx, cy))
            screen.blit(tower_img, tower_rect.topleft)
        else:
            pygame.draw.circle(screen, (0, 0, 255), (cx, cy), 30)

    if not wave_started:
        wave_enemies = create_wave_enemies(waves[current_wave])
        delay = 1
        for i, (kind, path, speed, frames) in enumerate(wave_enemies):
            delay_time = 10.0 if kind == 'boss' else i * delay
            spawn_queue.append((delay_time, kind, path, speed, frames))
        wave_started = True

    spawn_delay += dt
    new_queue = []
    for delay_time, kind, path, speed, frames in spawn_queue:
        if spawn_delay >= delay_time:
            enemies.append(Enemy(kind, path, speed, frames))
        else:
            new_queue.append((delay_time, kind, path, speed, frames))
    spawn_queue = new_queue

    if current_wave < len(waves) - 1:
        wave_timer += dt
        if wave_timer >= wave_duration or (all(not e.alive for e in enemies) and not spawn_queue):
            player_cash += (current_wave + 1) * 50 # Cash reward for completing wave
            current_wave += 1
            wave_timer = 0
            wave_started = False
            spawn_queue.clear()
            spawn_delay = 0
    else:
        if all(not e.alive for e in enemies) and not spawn_queue:
            wave_started = False
            spawn_queue.clear()
            spawn_delay = 0

    for enemy in enemies:
        if enemy.alive:
            enemy.update(dt)

    for tower in tower_objects:
        tower.update(enemies, dt)

    for enemy in enemies:
        if enemy.alive:
            pass
        elif not hasattr(enemy, 'cash_given'):
            kind = enemy.kind
            player_cash += enemy_cash_values.get(kind, 0)
            enemy.cash_given = True # Prevent giving cash multiple times

    for enemy in enemies:
        if enemy.alive:
            enemy.draw(screen)

    wave_text = font.render(f"Wave: {current_wave + 1}/{len(waves)}", True, (255, 255, 255))
    time_remaining = max(0, int(wave_duration - wave_timer))
    timer_text = font.render(f"Time: {time_remaining}s", True, (255, 255, 255))
    screen.blit(wave_text, (10, 10))
    screen.blit(timer_text, (10, 50))
    cash_text = font.render(f"Cash: ${player_cash}", True, (255, 255, 0))
    screen.blit(cash_text, (1100, 750))
    pygame.display.flip()