# Chicken Invaders - Technical Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Code Architecture](#code-architecture)
3. [Core Components](#core-components)
4. [Game States](#game-states)
5. [Class Documentation](#class-documentation)
6. [Game Mechanics](#game-mechanics)
7. [Asset Management](#asset-management)
8. [Event Handling](#event-handling)
9. [Performance Considerations](#performance-considerations)
10. [Development Guidelines](#development-guidelines)

## Project Overview

Chicken Invaders is a Python-based space shooter game built using the Pygame library. The game features a modular architecture with clear separation of concerns between different components.

### Key Technologies
- Python 3.x
- Pygame
- JSON for data storage
- PIL (Python Imaging Library) for image processing

## Code Architecture

### Main Components
```
Mainv10.py
├── AssetLoader
├── ChickenType
├── Player
├── Enemy
├── Bullet
├── Missile
├── Explosion
├── PowerUp
├── Button
├── Shop
└── Game
```

### File Structure
```
Chicken Invaders/
├── Mainv10.py
├── Images/
│   ├── Objects/
│   │   ├── Chickens/
│   │   ├── Spacecraft/
│   │   ├── Fire/
│   │   ├── Missile/
│   │   ├── Boom/
│   │   └── Gifts/
│   └── Textures/
├── Sounds/
└── high_scores.json
```

## Core Components

### 1. Game Initialization
```python
pygame.init()
mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
FPS = 60
```
- Initializes Pygame and its sound mixer
- Sets up basic game constants
- Configures display dimensions and frame rate

### 2. Game States
```python
INTRO = -1
MENU = 0
PLAYING = 1
GAME_OVER = 2
SHOP = 3
LEVEL_TRANSITION = 4
PAUSED = 5
SETTINGS = 6
NAME_INPUT = 7
HIGH_SCORES = 8
ABOUT = 9
```
Each state represents a different game screen or mode, managed by the main game loop.

## Class Documentation

### AssetLoader Class
```python
class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def load_assets(self):
        # Load and scale background
        self.images['background'] = pygame.image.load(
            os.path.join('Images', 'Textures', 'stars_galaxy.jpg')).convert()
        self.images['background'] = pygame.transform.scale(
            self.images['background'], (self.screen_width, self.screen_height))

        # Load player ships with alpha channel
        self.images['player'] = pygame.image.load(os.path.join(
            'Images', 'Objects', 'Spacecraft', 'ship2.png')).convert_alpha()
        
        # Scale images based on screen size
        base_size = int(min(self.screen_width, self.screen_height) * 0.07)
        self.images['player'] = pygame.transform.scale(
            self.images['player'], (base_size, base_size))
```

#### Detailed Asset Loading Process
1. Image Loading:
```python
# Example of loading and scaling a sprite
def load_sprite(self, path, scale_factor=1.0):
    image = pygame.image.load(path).convert_alpha()
    base_size = int(min(self.screen_width, self.screen_height) * scale_factor)
    return pygame.transform.scale(image, (base_size, base_size))
```

2. Sound Loading:
```python
def load_sound(self, path, volume=0.5):
    sound = mixer.Sound(path)
    sound.set_volume(volume)
    return sound
```

### ChickenType Class
```python
class ChickenType:
    def __init__(self, name, image_path, health, speed, points, behavior_type, special_ability=None):
        self.name = name
        self.image_path = image_path
        self.health = health
        self.speed = speed
        self.points = points
        self.behavior_type = behavior_type
        self.special_ability = special_ability

    @staticmethod
    def get_chicken_types():
        return {
            'ordinary_regular': ChickenType(
                'Ordinary Chicken',
                'Images/Objects/Chickens/OrdinaryChickenRegular.png',
                30, 2, 50, 'straight'
            ),
            'military': ChickenType(
                'Military Chicken',
                'Images/Objects/Chickens/OrdinaryChickenMilitary.png',
                40, 3, 75, 'zigzag'
            ),
            # More chicken types...
        }
```

#### Chicken Type Configuration Example
```python
# Example of creating a new chicken type
new_chicken = ChickenType(
    name='Boss Chicken',
    image_path='Images/Objects/Chickens/BossChicken.png',
    health=200,
    speed=1.5,
    points=1000,
    behavior_type='circle',
    special_ability='shield'
)
```

### Player Class
```python
class Player(pygame.sprite.Sprite):
    def __init__(self, assets, game, ship_type='default'):
        super().__init__()
        self.assets = assets
        self.game = game
        self.ship_type = ship_type
        self.set_ship_image()
        
        # Initialize player properties
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.screen.get_width() // 2
        self.rect.bottom = self.game.screen.get_height() - 20
        self.speed = int(self.game.screen.get_width() * 0.01)
        self.health = 100
        self.max_health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.power = 1
        self.missiles = 3
        self.shield = 0
```

#### Player Movement Example
```python
def update(self):
    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        self.rect.x -= self.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        self.rect.x += self.speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        self.rect.y -= self.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        self.rect.y += self.speed

    # Keep player on screen
    self.rect.clamp_ip(self.game.screen.get_rect())
```

#### Player Shooting Example
```python
def shoot(self):
    now = pygame.time.get_ticks()
    if now - self.last_shot > self.shoot_delay:
        self.last_shot = now
        if self.power == 1:
            # Single shot
            bullet = Bullet(self.rect.centerx, self.rect.top, self.game)
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)
        elif self.power >= 2:
            # Double shot
            bullet1 = Bullet(self.rect.left, self.rect.centery, self.game)
            bullet2 = Bullet(self.rect.right, self.rect.centery, self.game)
            self.game.all_sprites.add(bullet1, bullet2)
            self.game.bullets.add(bullet1, bullet2)
```

### Enemy Class
```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets, chicken_type, game):
        super().__init__()
        self.assets = assets
        self.game = game
        self.chicken_type = chicken_type
        self.set_enemy_image()
        
        # Initialize enemy properties
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, self.game.screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = chicken_type.speed
        self.health = chicken_type.health
        self.points = chicken_type.points
```

#### Enemy Movement Patterns
```python
def update(self):
    # Straight movement
    if self.behavior_type == 'straight':
        self.rect.y += self.speedy
    
    # Zigzag movement
    elif self.behavior_type == 'zigzag':
        self.rect.y += self.speedy
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.005) * 3
    
    # Circular movement
    elif self.behavior_type == 'circle':
        self.angle += 0.02
        self.rect.centerx = self.circle_center[0] + math.cos(self.angle) * self.circle_radius
        self.rect.centery = self.circle_center[1] + math.sin(self.angle) * self.circle_radius
        self.circle_center = (self.circle_center[0], self.circle_center[1] + 0.5)
    
    # Dive movement
    elif self.behavior_type == 'dive':
        if self.dive_timer == 0:
            self.rect.y += self.speedy
        else:
            self.rect.y += self.speedy * 2
        self.rect.x += self.speedx
        self.dive_timer = (self.dive_timer + 1) % 120
```

### Game Class
```python
class Game:
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Chicken Invaders")
        
        # Initialize game components
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = INTRO
        self.level = 1
        self.max_levels = 25
        
        # Load assets
        self.assets = AssetLoader()
        self.assets.screen_width = self.screen_width
        self.assets.screen_height = self.screen_height
        self.assets.load_assets()
```

#### Game Loop Example
```python
def run(self):
    last_enemy_spawn = pygame.time.get_ticks()
    while self.running:
        self.clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    self.state = PAUSED
        
        # Game state updates
        if self.state == PLAYING:
            # Spawn enemies
            now = pygame.time.get_ticks()
            if now - last_enemy_spawn > self.enemy_spawn_rate:
                self.spawn_enemy()
                last_enemy_spawn = now
            
            # Update game objects
            self.all_sprites.update()
            self.check_collisions()
            self.check_level_complete()
        
        # Rendering
        self.screen.blit(self.assets.images['background'], (0, 0))
        if self.state == PLAYING:
            self.all_sprites.draw(self.screen)
            self.draw_hud()
        
        pygame.display.flip()
```

## Game Mechanics

### Collision Detection System
```python
def check_collisions(self):
    # Bullet-Enemy collisions
    hits = pygame.sprite.groupcollide(
        self.enemies_group, self.bullets, False, True)
    for enemy, bullets in hits.items():
        for bullet in bullets:
            enemy.health -= bullet.damage
            if enemy.health <= 0:
                enemy.kill()
                self.player.add_score(enemy.points)
                self.create_explosion(enemy.rect.center)
    
    # Player-Enemy collisions
    hits = pygame.sprite.spritecollide(
        self.player, self.enemies_group, True, pygame.sprite.collide_mask)
    for enemy in hits:
        if self.player.take_damage(enemy.damage):
            self.game_over()
```

### Power-up System
```python
def spawn_powerup(self, center):
    # Define power-up types and their weights
    power_types = ['health', 'power', 'missile', 'shield']
    weights = [0.4, 0.3, 0.2, 0.1]
    
    # Adjust weights based on player state
    if self.player.health >= self.player.max_health * 0.8:
        weights[0] = 0.2
        weights[1] = 0.4
    
    # Select and create power-up
    power_type = random.choices(power_types, weights=weights, k=1)[0]
    powerup = PowerUp(center, power_type, self.assets)
    self.all_sprites.add(powerup)
    self.powerups.add(powerup)
```

### Level System
```python
def start_level(self):
    # Clear existing enemies
    for enemy in self.enemies_group:
        enemy.kill()
    
    # Get chicken type for current level
    chicken_type_key = self.chicken_type_keys[min(
        self.level - 1, len(self.chicken_type_keys) - 1)]
    chicken_type = self.chicken_types[chicken_type_key]
    
    # Calculate number of enemies
    self.enemies_per_level = 5 + (self.level - 1)
    self.enemies_remaining = self.enemies_per_level
    
    # Spawn initial enemies
    for _ in range(min(5, self.enemies_per_level)):
        self.spawn_enemy()
```

## Asset Management

### Image Loading System
```python
def load_assets(self):
    # Load and scale background
    self.images['background'] = pygame.image.load(
        os.path.join('Images', 'Textures', 'stars_galaxy.jpg')).convert()
    self.images['background'] = pygame.transform.scale(
        self.images['background'], (self.screen_width, self.screen_height))
    
    # Load player ships
    ship_paths = {
        'default': 'ship2.png',
        'blue': 'CIUShip.png',
        'red': 'CIUIonBlasterLV5.png'
    }
    
    for ship_type, path in ship_paths.items():
        self.images[f'player_{ship_type}'] = pygame.image.load(
            os.path.join('Images', 'Objects', 'Spacecraft', path)).convert_alpha()
        self.images[f'player_{ship_type}'] = pygame.transform.scale(
            self.images[f'player_{ship_type}'], (base_size, base_size))
```

### Sound Management System
```python
def load_sounds(self):
    # Load sound effects
    sound_paths = {
        'shoot': 'Sounds/gunshot.wav',
        'explosion': 'Sounds/explosion.wav',
        'powerup': 'Sounds/powerup.wav',
        'hit': 'Sounds/hit.wav'
    }
    
    for sound_name, path in sound_paths.items():
        try:
            self.assets.sounds[sound_name] = mixer.Sound(path)
            self.assets.sounds[sound_name].set_volume(0.5)
        except:
            print(f"Failed to load sound: {path}")
    
    # Load and play background music
    try:
        mixer.music.load('Sounds/Epic Hip Hop.wav')
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)  # Loop indefinitely
    except:
        print("Failed to load background music")
```

## Event Handling

### Input Processing System
```python
def handle_input(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.shoot()
            elif event.key == pygame.K_m:
                self.player.shoot_missile()
            elif event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_click(event.pos)
```

### Menu System
```python
def draw_menu(self):
    # Draw semi-transparent background
    s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    self.screen.blit(s, (0, 0))
    
    # Draw title
    title = self.assets.fonts['large'].render("SPACE HUNTER", True, WHITE)
    self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 100))
    
    # Draw buttons
    for button in self.menu_buttons:
        button.draw(self.screen)
```

## Performance Optimization

### Sprite Group Management
```python
def optimize_sprite_groups(self):
    # Create sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.enemies_group = pygame.sprite.Group()
    self.bullets = pygame.sprite.Group()
    self.missiles = pygame.sprite.Group()
    self.powerups = pygame.sprite.Group()
    self.explosions = pygame.sprite.Group()
    
    # Add player to groups
    self.player = Player(self.assets, self)
    self.all_sprites.add(self.player)
```

### Image Caching
```python
def cache_images(self):
    # Pre-load and scale commonly used images
    self.image_cache = {}
    for image_name, path in self.image_paths.items():
        try:
            image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(
                image, (self.base_size, self.base_size))
            self.image_cache[image_name] = scaled_image
        except:
            print(f"Failed to cache image: {path}")
```

## Development Guidelines

### Code Style Example
```python
# Good example
def calculate_damage(self, base_damage, power_level):
    """
    Calculate damage based on base damage and power level.
    
    Args:
        base_damage (int): Base damage value
        power_level (int): Current power level
        
    Returns:
        int: Calculated damage value
    """
    return base_damage * (1 + (power_level - 1) * 0.5)

# Bad example
def dmg(b, p):  # Unclear variable names
    return b * (1 + (p - 1) * 0.5)  # No documentation
```

### Error Handling
```python
def load_resource(self, path, resource_type):
    try:
        if resource_type == 'image':
            return pygame.image.load(path).convert_alpha()
        elif resource_type == 'sound':
            return mixer.Sound(path)
        else:
            raise ValueError(f"Unknown resource type: {resource_type}")
    except pygame.error as e:
        print(f"Failed to load {resource_type} from {path}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading {resource_type}: {e}")
        return None
```

## Conclusion

This enhanced documentation provides detailed code examples and explanations for the Chicken Invaders codebase. Each section includes practical examples that demonstrate the implementation of various game features and systems.

For further assistance or clarification, please contact the development team.

---

*Last updated: [Current Date]*
*Version: 1.1* 