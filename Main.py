import logging
import pygame
import random
import os
import json
from pygame import mixer  # for sound
import math

# Initialize pygame
pygame.init()
mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
FPS = 60  # Frames Per Second


# todo use in self.state = [ ??? ]
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

# Colors use in menu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


OBJECT_SIZES = {
    # Player ships
    'player_default': 0.07,
    'player_blue': 0.07,
    'player_gray': 0.07,
    'player_green': 0.07,
    'player_orange': 0.07,
    'player_red': 0.07,
    'player_white': 0.07,

    # Enemy chickens
    'ordinary chicken': 0.09,
    'military chicken': 0.09,
    'drone chicken': 0.06,
    'pilot chicken': 0.09,
    'phoenix chicken': 0.2,
    'metal chicken': 0.09,
    'metal military chicken': 0.09,
    'metal pudgy chicken': 0.08,
    'coward chicken': 0.06,
    'toxic chicken': 0.09,
    'balloon chicken': 0.08,
    'klaus chicken': 0.09,
    'chiller 1': 0.09,
    'chiller 2': 0.09,
    'chiller 3': 0.09,
    'ufo chicken': 0.08,
    'submarine chicken': 0.09,
    'slob chicken': 0.09,
    'chickenaut': 0.09,
    'egg ship chicken': 0.08,
    'big chicken': 0.1,
    'super chicken': 0.08,
    'infini chicken': 0.09,
    'feather brain': 0.09,
    'yolk star': 0.12,

    # Projectiles
    'bullet': 0.035,
    'missile': 0.06,

    # Effects
    'explosion_small': 0.07,
    'explosion_large': 0.1,
    'powerup_health': 0.06,
    'powerup_power': 0.05,
    'powerup_missile': 0.05,
    'powerup_shield': 0.05,
    'heart': 0.06,
}


class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def get_object_size(self, object_type):
        # Get the size ratio from OBJECT_SIZES, default to 0.07 if not found
        size_ratio = OBJECT_SIZES.get(object_type.lower(), 0.07)
        # Calculate the actual size in pixels
        base_size = int(
            min(self.screen_width, self.screen_height) * size_ratio)
        return base_size


# ? Shof al HowPygameWork.py 3lashn t explain what is happend usin pygame.
# ? 1. Load image from path.
# ? 2. convert_alpha if PNG or convert if image.
# ? 3. scale or rotate or not.
# ? 4. draw in screen by block image transfer [blit] and fill Update the full screen

    def load_assets(self):
        # Load images
        self.images['background'] = pygame.image.load(
            os.path.join('Images', 'Textures', 'stars_galaxy.jpg')).convert()
        self.images['background'] = pygame.transform.scale(self.images['background'],
                                                           (self.screen_width, self.screen_height))
        self.images['background_blurred'] = pygame.image.load(os.path.join(
            'Images', 'Textures', 'stars_galaxy_bullured.jpg')).convert()
        self.images['background_blurred'] = pygame.transform.scale(self.images['background_blurred'],
                                                                   (self.screen_width, self.screen_height))

        # Player ships with individual sizes
        player_ships = {
            'player': 'ship2.png',
            'player_blue': 'CIUShip.png',
            'player_gray': 'VF.png',
            'player_green': 'BX.png',
            'player_orange': 'HnC.png',
            'player_red': 'CIUIonBlasterLV5.png',
            'player_white': 'HenSoloCI4.png'
        }

        for ship_key, ship_file in player_ships.items():
            self.images[ship_key] = pygame.image.load(os.path.join(
                'Images', 'Objects', 'Spacecraft', ship_file)).convert_alpha()
            ship_size = self.get_object_size(ship_key)
            self.images[ship_key] = pygame.transform.scale(
                self.images[ship_key], (ship_size, ship_size))
            self.images[ship_key] = pygame.transform.rotate(
                self.images[ship_key], 0)

        # Projectiles
        self.images['bullet'] = pygame.image.load(os.path.join(
            'Images', 'Objects', 'Fire', 'IonBlasterSingle.png')).convert_alpha()
        self.images['missile'] = pygame.image.load(os.path.join(
            'Images', 'Objects', 'Missile', 'missile.png')).convert_alpha()

        bullet_size = self.get_object_size('bullet')
        missile_size = self.get_object_size('missile')
        self.images['bullet'] = pygame.transform.scale(
            self.images['bullet'], (bullet_size, bullet_size))
        self.images['missile'] = pygame.transform.scale(
            self.images['missile'], (missile_size, missile_size))

        # Effects
        self.images['explosion1'] = pygame.image.load(
            os.path.join('Images', 'Objects', 'Boom', 'Boomv1.png')).convert_alpha()
        self.images['explosion2'] = pygame.image.load(
            os.path.join('Images', 'Objects', 'Boom', 'Boomv2.png')).convert_alpha()
        self.images['heart'] = pygame.image.load(os.path.join(
            'Images', 'Objects', 'Gifts', 'Heart.png')).convert_alpha()

        explosion_small_size = self.get_object_size('explosion_small')
        explosion_large_size = self.get_object_size('explosion_large')
        heart_size = self.get_object_size('heart')

        self.images['explosion1'] = pygame.transform.scale(
            self.images['explosion1'], (explosion_small_size, explosion_small_size))
        self.images['explosion2'] = pygame.transform.scale(
            self.images['explosion2'], (explosion_large_size, explosion_large_size))
        self.images['heart'] = pygame.transform.scale(
            self.images['heart'], (heart_size, heart_size))

        # Load fonts
        font_scale = int(self.screen_width / 20)
        self.fonts['large'] = pygame.font.Font(None, font_scale)
        self.fonts['medium'] = pygame.font.Font(None, int(font_scale * 0.7))
        self.fonts['small'] = pygame.font.Font(None, int(font_scale * 0.5))


class ChickenType:
    def __init__(self, name, image_path, health, speed, points, behavior_type, special_ability=None):
        self.name = name
        self.image_path = image_path
        self.health = health
        self.speed = speed
        self.points = points
        # straight, zigzag, shoot, circle, float, teleport, dive, flee
        self.behavior_type = behavior_type
        # shield, freeze, resurrect, poison, eat, transform, clone, smart, boss, powerup, final_boss
        self.special_ability = special_ability

    @staticmethod  # static method to get chicken types
    def get_chicken_types():
        return {
            'ordinary_regular': ChickenType('Ordinary Chicken', 'Images/Objects/Chickens/OrdinaryChickenRegular.png', 30, 2, 50, 'straight'),
            'ordinary_military': ChickenType('Military Chicken', 'Images/Objects/Chickens/OrdinaryChickenMilitary.png', 40, 3, 75, 'zigzag'),
            'drone': ChickenType('Drone Chicken', 'Images/Objects/Chickens/DroneChicken.png', 25, 4, 100, 'straight', 'shoot'),
            'pilot': ChickenType('Pilot Chicken', 'Images/Objects/Chickens/PilotChicken.png', 35, 5, 125, 'dive'),
            'phoenix': ChickenType('Phoenix Chicken', 'Images/Objects/Chickens/Phoenix_Chicken_.png', 70, 4, 400, 'straight', 'resurrect'),
            'metal_regular': ChickenType('Metal Chicken', 'Images/Objects/Chickens/MetalSuitChickenRegular.png', 60, 2, 150, 'straight', 'shield'),
            'metal_military': ChickenType('Metal Military Chicken', 'Images/Objects/Chickens/MetalSuitChickenMilitary.png', 70, 3, 175, 'zigzag', 'shield'),
            'metal_pudgy': ChickenType('Metal Pudgy Chicken', 'Images/Objects/Chickens/MetalSuitChickenPudgy.png', 80, 1, 200, 'straight', 'shield'),
            'coward': ChickenType('Coward Chicken', 'Images/Objects/Chickens/CowardChicken.png', 20, 6, 225, 'flee'),
            'toxic': ChickenType('Toxic Chicken', 'Images/Objects/Chickens/ToxicChicken.png', 45, 2, 250, 'straight', 'poison'),
            'balloon': ChickenType('Balloon Chicken', 'Images/Objects/Chickens/BalloonChicken7.png', 30, 3, 275, 'float'),
            'klaus': ChickenType('Klaus Chicken', 'Images/Objects/Chickens/KlausChicken.png', 90, 2, 300, 'straight', 'boss'),
            'chiller1': ChickenType('Chiller 1', 'Images/Objects/Chickens/Chiller1.png', 40, 3, 325, 'straight', 'freeze'),
            'chiller2': ChickenType('Chiller 2', 'Images/Objects/Chickens/Chiller2.png', 50, 4, 350, 'zigzag', 'freeze'),
            'chiller3': ChickenType('Chiller 3', 'Images/Objects/Chickens/Chiller3.png', 60, 5, 375, 'circle', 'freeze'),
            'ufo': ChickenType('UFO Chicken', 'Images/Objects/Chickens/UFOChicken.png', 55, 5, 425, 'teleport'),
            'submarine': ChickenType('Submarine Chicken', 'Images/Objects/Chickens/SubmarineChicken.PNG.png', 65, 3, 450, 'dive', 'submerge'),
            'slob': ChickenType('Slob Chicken', 'Images/Objects/Chickens/SlobChicken.png', 100, 1, 475, 'straight', 'eat'),
            'chickenaut': ChickenType('Chickenaut', 'Images/Objects/Chickens/Chickenaut.PNG.png', 75, 4, 500, 'straight', 'transform'),
            'eggship': ChickenType('Egg Ship Chicken', 'Images/Objects/Chickens/EggShipChicken.png', 85, 3, 525, 'straight', 'spawn'),
            'big': ChickenType('Big Chicken', 'Images/Objects/Chickens/BigChickenCI4.png', 150, 2, 550, 'straight', 'boss'),
            'super': ChickenType('Super Chicken', 'Images/Objects/Chickens/CI4_SuperChick.png', 120, 4, 575, 'zigzag', 'powerup'),
            'infini': ChickenType('Infini Chicken', 'Images/Objects/Chickens/CI4_InfiniChick.png', 200, 3, 600, 'straight', 'clone'),
            'featherbrain': ChickenType('Feather Brain', 'Images/Objects/Chickens/FeatherBrain.png', 80, 5, 625, 'circle', 'smart'),
            'yolkstar': ChickenType('Yolk Star', 'Images/Objects/Chickens/YolkStar.png', 250, 2, 1000, 'straight', 'final_boss')
        }


class Player(pygame.sprite.Sprite):
    def __init__(self, assets, game, ship_type='default'):
        super().__init__()
        self.assets = assets
        self.game = game
        self.ship_type = ship_type
        self.set_ship_image()
        # It is an invisible box used to locate the ship on the screen and clashes
        # get the rect of the image and creates a rectangle for IMAGE
        self.rect = self.image.get_rect()
        # center the rect on the screen
        self.rect.centerx = self.game.screen.get_width() // 2
        self.rect.bottom = self.game.screen.get_height() - 20  # bottom of the rect
        # Scale speed with screen size
        self.speed = int(self.game.screen.get_width() * 0.01)
        self.health = 100
        self.max_health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()  # ! Back Here
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.score = 0
        self.missiles = 3
        self.side_guns = False  # ! Single Double Quadruple

    def set_ship_image(self):
        # Use the selected spacecraft from settings
        if self.game.selected_spacecraft:
            img_path = os.path.join(
                'Images', 'Objects', 'Spacecraft', self.game.selected_spacecraft)
            self.image = pygame.image.load(img_path).convert_alpha()
            base_size = int(min(self.game.screen.get_width(),
                            self.game.screen.get_height()) * 0.07)
            self.image = pygame.transform.scale(
                self.image, (base_size, base_size))
        else:
            self.image = pygame.Surface((60, 60))
            self.image.fill((255, 0, 0))  # ! Red
        self.mask = pygame.mask.from_surface(
            self.image)  # collisions between the chiken

    def update(self):
        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:  # ! b3mlha when Game over
            self.hidden = False
            self.rect.centerx = self.game.screen.get_width() // 2
            self.rect.bottom = self.game.screen.get_height() - 20

        # Reset speed and shoot delay if freeze effect ends
        if pygame.time.get_ticks() - self.game.freeze_timer > 3000:
            self.speed = int(self.game.screen.get_width() *
                             0.01)  # Reset to default speed
            self.shoot_delay = 250  # Reset to default shoot delay

        # Power down if powerup time expires
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power = 1
            self.side_guns = False

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
        # 3lashan matl3sh bra al Fram bt3 al screen + can move into it
        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:  # This prevents shooting at an illogical speed
            self.last_shot = now
            if self.power == 1:  # single shot
                bullet = Bullet(self.rect.centerx, self.rect.top,
                                self.game)  # drawn and treated
                self.game.all_sprites.add(bullet)
                self.game.bullets.add(bullet)
                self.assets.sounds['shoot'].play()
            elif self.power >= 2:  # double shot
                bullet1 = Bullet(self.rect.left, self.rect.centery, self.game)
                bullet2 = Bullet(self.rect.right, self.rect.centery, self.game)
                self.game.all_sprites.add(bullet1, bullet2)
                self.game.bullets.add(bullet1, bullet2)
                self.assets.sounds['shoot'].play()
                if self.side_guns:
                    bullet3 = Bullet(self.rect.centerx,
                                     self.rect.top, self.game, -15)  # Two additional bullets from the center, but with two teaspoons
                    bullet4 = Bullet(self.rect.centerx,
                                     self.rect.top, self.game, 15)  # Two additional bullets from the center, but with two teaspoons
                    self.game.all_sprites.add(bullet3, bullet4)
                    self.game.bullets.add(bullet3, bullet4)

    def shoot_missile(self):
        if self.missiles > 0:
            missile = Missile(self.rect.centerx, self.rect.top,
                              self.assets, self.game)  # drawn and treated
            self.game.all_sprites.add(missile)
            self.game.missiles.add(missile)
            self.missiles -= 1
            self.assets.sounds['shoot'].play()

    def hide(self):  # temporarily hide the player when life is lost
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (self.game.screen.get_width() //
                            2, self.game.screen.get_height() + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        if self.power >= 3:
            self.side_guns = True

    def take_damage(self, amount):
        self.health -= amount
        self.assets.sounds['hit'].play()
        if self.health <= 0:
            self.lives -= 1
            self.health = self.max_health
            self.hide()
            if self.lives <= 0:
                return True
        return False

    def add_score(self, points):
        self.score += points


class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets, chicken_type, game):
        super().__init__()
        self.assets = assets
        self.game = game
        self.chicken_type = chicken_type
        self.set_enemy_image()

        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        # the object starts outside the screen
        self.rect.y = random.randrange(-150, -100)

        # Initialize movement variables
        self.speedy = chicken_type.speed
        self.speedx = 0
        self.health = chicken_type.health
        self.damage = 10
        self.points = chicken_type.points

        # Behavior specific variables
        self.behavior_type = chicken_type.behavior_type
        self.special_ability = chicken_type.special_ability
        self.angle = 0
        self.circle_radius = 100
        self.circle_center = (screen_width // 2, -100)
        self.teleport_timer = 0
        self.dive_timer = 0
        self.shield_active = False
        self.freeze_timer = 0
        self.resurrected = False
        self.submerged = False
        self.transform_timer = 0
        self.clone_timer = 0
        self.smart_timer = 0

    def set_enemy_image(self):
        self.image = pygame.image.load(
            self.chicken_type.image_path).convert_alpha()
        # Use the exact chicken type name for size lookup
        enemy_size = self.game.assets.get_object_size(
            self.chicken_type.name.lower())
        self.image = pygame.transform.scale(
            self.image, (enemy_size, enemy_size))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()

        # Update behavior based on chicken type
        if self.behavior_type == 'straight':
            self.rect.y += self.speedy

        elif self.behavior_type == 'zigzag':
            self.rect.y += self.speedy
            self.rect.x += math.sin(pygame.time.get_ticks() * 0.005) * 3

        elif self.behavior_type == 'circle':
            self.angle += 0.02
            self.rect.centerx = self.circle_center[0] + \
                math.cos(self.angle) * self.circle_radius
            self.rect.centery = self.circle_center[1] + \
                math.sin(self.angle) * self.circle_radius
            self.circle_center = (
                self.circle_center[0], self.circle_center[1] + 0.5)

        elif self.behavior_type == 'dive':
            if self.dive_timer == 0:
                self.rect.y += self.speedy
            else:
                self.rect.y += self.speedy * 2
            self.rect.x += self.speedx
            self.dive_timer = (self.dive_timer + 1) % 120

        elif self.behavior_type == 'flee':
            if self.rect.centerx < self.game.player.rect.centerx:
                self.rect.x -= self.speedy
            else:
                self.rect.x += self.speedy
            self.rect.y += self.speedy * 0.5

        elif self.behavior_type == 'float':
            self.rect.y += self.speedy * 0.5
            self.rect.x += math.sin(pygame.time.get_ticks() * 0.003) * 2

        elif self.behavior_type == 'teleport':
            if pygame.time.get_ticks() - self.teleport_timer > 2000:
                self.rect.x = random.randrange(
                    0, screen_width - self.rect.width)
                self.teleport_timer = pygame.time.get_ticks()

        # Handle special abilities
        if self.special_ability == 'shield' and self.health < self.chicken_type.health * 0.5:
            self.shield_active = True

        if self.special_ability == 'freeze':
            # Freeze beam effect
            if pygame.time.get_ticks() - self.freeze_timer > 3000:
                # Apply freeze effect to player
                self.game.player.shoot_delay *= 1.5
                self.game.player.speed *= 0.7
                # Create ice particles
                self.create_ice_particles()
                self.freeze_timer = pygame.time.get_ticks()
                # Play freeze sound
                if 'freeze' in self.game.assets.sounds:
                    self.game.assets.sounds['freeze'].play()

        if self.special_ability == 'resurrect' and self.health <= 0 and not self.resurrected:
            self.health = self.chicken_type.health * 0.5
            self.resurrected = True

        if self.special_ability == 'submerge' and pygame.time.get_ticks() % 2000 < 1000:
            self.submerged = True
            self.rect.y += self.speedy * 0.5
        else:
            self.submerged = False

        if self.special_ability == 'transform' and pygame.time.get_ticks() - self.transform_timer > 5000:
            self.speedy *= 1.5
            self.transform_timer = pygame.time.get_ticks()

        if self.special_ability == 'clone' and pygame.time.get_ticks() - self.clone_timer > 10000:
            new_enemy = Enemy(self.assets, self.chicken_type, self.game)
            new_enemy.rect.x = self.rect.x + 50
            new_enemy.rect.y = self.rect.y
            self.game.all_sprites.add(new_enemy)
            self.game.enemies_group.add(new_enemy)
            self.clone_timer = pygame.time.get_ticks()

        if self.special_ability == 'smart':
            if pygame.time.get_ticks() - self.smart_timer > 2000:
                dx = self.game.player.rect.centerx - self.rect.centerx
                dy = self.game.player.rect.centery - self.rect.centery
                dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                self.speedx = dx / dist * self.speedy
                self.smart_timer = pygame.time.get_ticks()

        # Keep enemy on screen
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.speedx *= -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx *= -1

        # Respawn at top if off screen bottom
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(0, screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = self.chicken_type.speed

    def create_ice_particles(self):
        # Create ice particles for visual effect
        for _ in range(5):
            particle = IceParticle(self.rect.center, self.game.assets)
            self.game.all_sprites.add(particle)
            self.game.particles.add(particle)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game, angle=0):
        super().__init__()
        self.game = game
        # Use the selected fire image from settings
        if self.game.selected_fire:
            img_path = os.path.join(
                'Images', 'Objects', 'Fire', self.game.selected_fire)
            self.image = pygame.image.load(img_path).convert_alpha()
            bullet_size = int(min(self.game.screen.get_width(),
                              self.game.screen.get_height()) * 0.07 * 0.5)
            self.image = pygame.transform.scale(
                self.image, (bullet_size, bullet_size))
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 255, 0))  # yellow
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.angle = angle
        self.damage = 25
        if angle != 0:
            self.image = pygame.transform.rotate(self.image, angle)
            self.speedx = 5 if angle < 0 else -5

    def update(self):
        self.rect.y += self.speedy
        if hasattr(self, 'speedx'):
            self.rect.x += self.speedx

        # Kill if off screen and Delete the bullet out of the screen
        if self.rect.bottom < 0 or self.rect.top > self.game.screen.get_height() or self.rect.left > self.game.screen.get_width() or self.rect.right < 0:
            self.kill()


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, assets, game):
        super().__init__()
        self.assets = assets
        self.game = game
        # Use the selected missile image from settings
        if self.game.selected_missile:
            img_path = os.path.join(
                'Images', 'Objects', 'Missile', self.game.selected_missile)
            self.image = pygame.image.load(img_path).convert_alpha()
            bullet_size = int(min(self.assets.screen_width,
                              self.assets.screen_height) * 0.07 * 0.5)
            self.image = pygame.transform.scale(
                self.image, (bullet_size, bullet_size))
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -8
        self.damage = 50
        self.homing = True
        self.target = None

    def update(self):
        if self.homing:
            # Find the closest enemy
            if not self.target or not self.target.alive():
                enemies = [
                    e for e in self.game.enemies_group if e.rect.top < self.game.screen.get_height()]
                if enemies:
                    self.target = min(enemies, key=lambda e: ((e.rect.centerx - self.rect.centerx) ** 2 +
                                                              (e.rect.centery - self.rect.centery) ** 2) ** 0.5)

            if self.target:
                # Move toward target
                dx = self.target.rect.centerx - self.rect.centerx
                dy = self.target.rect.centery - self.rect.centery
                dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)

                self.rect.x += int(dx / dist * 5)
                self.rect.y += int(dy / dist * 5)
            else:
                self.rect.y += self.speedy
        else:
            self.rect.y += self.speedy

        # Kill if off screen
        if self.rect.bottom < 0 or self.rect.top > self.game.screen.get_height():
            self.kill()


class Explosion(pygame.sprite.Sprite):  # Boom
    def __init__(self, center, size, assets):
        super().__init__()
        self.assets = assets
        self.size = size
        self.image = self.assets.images['explosion1'] if size == 'small' else self.assets.images['explosion2']
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 8:
                self.kill()
            else:
                center = self.rect.center
                if self.size == 'small':
                    self.image = self.assets.images['explosion1']
                else:
                    self.image = self.assets.images['explosion2']
                self.rect = self.image.get_rect()
                self.rect.center = center


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, power_type, assets):
        super().__init__()
        self.assets = assets
        self.type = power_type
        if power_type == 'health' or power_type.lower() == 'heart.png':
            self.image = self.assets.images['heart']
        elif power_type == 'power':
            img_path = os.path.join(
                'Images', 'Objects', 'Gifts', 'GIFIonBlasterCI1.png')
            self.image = pygame.image.load(img_path).convert_alpha()
            powerup_size = self.assets.get_object_size('powerup_power')
            self.image = pygame.transform.scale(
                self.image, (powerup_size, powerup_size))
        elif power_type == 'missile':
            img_path = os.path.join(
                'Images', 'Objects', 'Gifts', 'GIFIonBlasterCI2.png')
            self.image = pygame.image.load(img_path).convert_alpha()
            powerup_size = self.assets.get_object_size('powerup_missile')
            self.image = pygame.transform.scale(
                self.image, (powerup_size, powerup_size))
        else:
            powerup_size = self.assets.get_object_size('powerup_health')
            self.image = pygame.Surface((powerup_size, powerup_size))
            self.image.fill((200, 200, 0))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > self.assets.screen_height:
            self.kill()


class Button:  # Button in menu
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class Shop:
    def __init__(self, assets):
        self.assets = assets
        self.items = [
            {'name': 'Health Boost', 'cost': 500,
                'description': 'Increase max health by 20%', 'type': 'health'},
            {'name': 'Faster Shooting', 'cost': 750,
                'description': 'Reduce shoot delay by 30%', 'type': 'shoot_speed'},
            {'name': 'Side Guns', 'cost': 1000,
                'description': 'Add two additional guns', 'type': 'side_guns'},
            {'name': 'Missile Pack', 'cost': 300,
                'description': '+3 missiles', 'type': 'missiles'},
            {'name': 'New Ship', 'cost': 1500,
                'description': 'Unlock a new ship type', 'type': 'ship'}
        ]
        self.buttons = []
        self.selected_ship = 'default'
        self.ship_options = ['default', 'blue', 'red', 'green', 'yellow']
        self.unlocked_ships = ['default']

        # Create buttons
        for i, item in enumerate(self.items):
            btn = Button(self.assets.screen_width//2 - 200, 150 + i*100, 400, 60,
                         f"{item['name']} - {item['cost']} pts",
                         GREEN, YELLOW)
            self.buttons.append(btn)

        self.back_button = Button(self.assets.screen_width//2 - 100, self.assets.screen_height - 100, 200, 50,
                                  "Back to Game", BLUE, YELLOW)

    def draw(self, surface, player_score):
        # Draw semi-transparent background
        s = pygame.Surface(
            (self.assets.screen_width, self.assets.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        surface.blit(s, (0, 0))

        # Draw title
        title = self.assets.fonts['large'].render("SHOP", True, WHITE)
        surface.blit(title, (self.assets.screen_width //
                     2 - title.get_width()//2, 50))

        # Draw score
        score_text = self.assets.fonts['medium'].render(
            f"Score: {player_score}", True, WHITE)
        surface.blit(score_text, (self.assets.screen_width //
                     2 - score_text.get_width()//2, 100))

        # Draw items
        for i, (item, btn) in enumerate(zip(self.items, self.buttons)):
            btn.draw(surface)

            # Draw description
            desc = self.assets.fonts['small'].render(
                item['description'], True, WHITE)
            surface.blit(desc, (self.assets.screen_width//2 -
                         desc.get_width()//2, btn.rect.bottom + 5))

        # Draw back button
        self.back_button.draw(surface)

    def handle_event(self, event, player):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        if self.back_button.is_clicked(mouse_pos, event):
            return 'back'
        for i, (item, btn) in enumerate(zip(self.items, self.buttons)):
            btn.check_hover(mouse_pos)
            if btn.is_clicked(mouse_pos, event):
                if player.score >= item['cost']:
                    self.apply_upgrade(player, item)
                    return 'purchase'
                else:
                    return 'fail'
        return None

    def apply_upgrade(self, player, item):
        player.score -= item['cost']

        if item['type'] == 'health':
            player.max_health = int(player.max_health * 1.2)
            player.health = player.max_health
        elif item['type'] == 'shoot_speed':
            player.shoot_delay = int(player.shoot_delay * 0.7)
        elif item['type'] == 'side_guns':
            player.side_guns = True
        elif item['type'] == 'missiles':
            player.missiles += 3
        elif item['type'] == 'shield':
            player.shield += 2
        elif item['type'] == 'ship':
            # Get available ship options from the game's spacecraft_options
            available_ships = [
                s for s in player.game.spacecraft_options if s not in self.unlocked_ships]
            if available_ships:
                new_ship = random.choice(available_ships)
                self.unlocked_ships.append(new_ship)
                # Update the game's selected spacecraft
                player.game.selected_spacecraft = new_ship
                # Update the player's ship image
                player.set_ship_image()
                # Play a sound effect for the ship change
                if 'powerup' in player.game.assets.sounds:
                    player.game.assets.sounds['powerup'].play()

    def buy_ship(self, ship_name):
        if ship_name in self.assets.images:
            self.game.selected_spacecraft = ship_name
            self.game.player.set_ship_image()  # Update the player's ship image immediately
            return True
        return False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Chicken Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.intro_played = False
        self.state = INTRO
        self.level = 1
        self.max_levels = 25
        self.player_name = ""
        self.name_input_active = True

        # Load assets with current screen size
        self.assets = AssetLoader()
        self.assets.screen_width = self.screen_width
        self.assets.screen_height = self.screen_height
        self.assets.load_assets()

        # Load chicken types
        self.chicken_types = ChickenType.get_chicken_types()
        self.chicken_type_keys = list(self.chicken_types.keys())

        # Game objects
        self.player = None
        self.all_sprites = None
        self.enemies_group = None
        self.bullets = None
        self.missiles = None
        self.powerups = None
        self.explosions = None

        # Level management
        self.enemies_per_level = 1  # Base number of enemies per level
        self.enemies_remaining = 0
        self.level_complete = False

        # UI elements
        self.create_menu_buttons()
        self.pause_button = Button(
            self.screen_width//2 - 100, self.screen_height//2 - 25, 200, 50, "Resume", GREEN, YELLOW)

        # Game settings
        self.difficulty = 1
        self.enemy_spawn_rate = 1000

        # High scores
        self.high_scores = []
        self.load_high_scores()

        # Shop
        self.shop = Shop(self.assets)

        # Load sounds
        self.load_sounds()

        # Intro assets
        self.intro_frames = self.load_gif_frames(os.path.join(
            'Images', 'Objects', 'WhenWon', 'emoji-dance.gif'))
        self.intro_frame_index = 0
        self.intro_start_time = pygame.time.get_ticks()
        self.intro_duration = 400000  # ms
        self.intro_sound_played = False

        # Settings selections (per session, now auto-detected)
        self.fire_options = [f for f in os.listdir(os.path.join(
            'Images', 'Objects', 'Fire')) if f.lower().endswith('.png')]
        self.spacecraft_options = [f for f in os.listdir(os.path.join(
            'Images', 'Objects', 'Spacecraft')) if f.lower().endswith('.png')]
        self.missile_options = [f for f in os.listdir(os.path.join(
            'Images', 'Objects', 'Missile')) if f.lower().endswith('.png')]
        self.selected_fire = self.fire_options[0] if self.fire_options else None
        self.selected_spacecraft = self.spacecraft_options[0] if self.spacecraft_options else None
        self.selected_missile = self.missile_options[0] if self.missile_options else None

        self.previous_state = None  # Track previous state for shop
        self.shop_message = ''
        self.shop_message_time = 0

        # Freeze effect timer
        self.freeze_timer = 0

        # Add new variables for level 5 sound
        self.level5_sound_played = False
        self.level5_sound_start_time = 0
        self.level5_sound_duration = 8000  # 8 seconds in milliseconds

        # Sound control variables
        self.menu_music_playing = False

    def load_gif_frames(self, gif_path):
        try:
            from PIL import Image  # for gif image
        except ImportError:
            print("PIL module not found. Please install Pillow to show animated GIFs.")
            return []
        frames = []
        try:
            img = Image.open(gif_path)
            for frame in range(0, img.n_frames):
                img.seek(frame)
                frame_image = img.convert('RGBA')
                mode = frame_image.mode
                size = frame_image.size
                data = frame_image.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)
                scale = min(self.screen_width // 2, self.screen_height // 2)
                py_image = pygame.transform.scale(py_image, (scale, scale))
                frames.append(py_image)
        except Exception as e:
            print(f"Error loading GIF: {e}")
        finally:
            return frames

    def load_sounds(self):
        # Load sound effects
        self.assets.sounds['shoot'] = mixer.Sound('Sounds/gunshot.wav')
        self.assets.sounds['explosion'] = mixer.Sound('Sounds/explosion.wav')
        self.assets.sounds['bomb'] = mixer.Sound('Sounds/bomb.wav')

        # Load intro sound
        try:
            self.intro_sound = mixer.Sound('Sounds/Intro.wav')
            self.intro_sound.set_volume(0.5)
        except:
            print("Failed to load intro sound")
            self.intro_sound = None

        # Load level 5 special sound
        try:
            self.level5_sound = mixer.Sound('Sounds/alml3b_wl3.wav')
            self.level5_sound.set_volume(0.5)
        except:
            print("Failed to load level 5 sound")
            self.level5_sound = None

        # Load background music
        try:
            self.menu_music = 'Sounds/Epic Hip Hop.wav'
        except:
            print("Failed to load menu music")
            self.menu_music = None

    def play_menu_music(self):
        if not self.menu_music_playing and self.menu_music:
            pygame.mixer.music.load(self.menu_music)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.menu_music_playing = True

    def stop_all_sounds(self):
        # Stop all sounds and music
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.menu_music_playing = False

    def create_menu_buttons(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        self.start_button = Button(
            center_x - 100, center_y - 50, 200, 50, "Start Game", GREEN, YELLOW)
        self.high_scores_button = Button(
            center_x - 100, center_y + 20, 200, 50, "High Scores", BLUE, YELLOW)
        self.about_button = Button(  # New About button
            center_x - 100, center_y + 90, 200, 50, "About", BLUE, YELLOW)
        self.quit_button = Button(
            center_x - 100, center_y + 160, 200, 50, "Quit", RED, YELLOW)

        self.menu_buttons = [self.start_button,
                             self.high_scores_button, self.about_button, self.quit_button]

        self.back_button = Button(
            center_x - 100, self.screen_height - 100, 200, 50, "Back", BLUE, YELLOW)
        self.next_button = Button(
            center_x - 100, center_y, 200, 50, "Next Level", GREEN, YELLOW)
        self.shop_button = Button(
            center_x - 100, center_y + 70, 200, 50, "Visit Shop", BLUE, YELLOW)
        self.restart_button = Button(
            center_x - 100, center_y, 200, 50, "Play Again", GREEN, YELLOW)
        self.menu_button = Button(
            center_x - 100, center_y + 70, 200, 50, "Main Menu", BLUE, YELLOW)
        self.settings_button = Button(
            self.screen_width//2 - 100, self.screen_height//2 + 230, 200, 50, "Settings", BLUE, YELLOW)

        self.menu_buttons.append(self.settings_button)

    def start_level(self):
        # Clear existing enemies
        for enemy in self.enemies_group:
            enemy.kill()

        # Get the chicken type for current level
        chicken_type_key = self.chicken_type_keys[min(
            self.level - 1, len(self.chicken_type_keys) - 1)]
        chicken_type = self.chicken_types[chicken_type_key]

        # Calculate number of enemies for this level
        self.enemies_per_level = 5 + (self.level - 1)
        self.enemies_remaining = self.enemies_per_level

        # Spawn initial enemies
        for _ in range(min(5, self.enemies_per_level)):
            self.spawn_enemy()

        # Reset level completion flag
        self.level_complete = False

        # Handle level 5 special sound
        if self.level == 5 and not self.level5_sound_played:
            self.stop_all_sounds()  # Stop any current sounds
            if self.level5_sound:
                self.level5_sound.play()
                self.level5_sound_played = True
                self.level5_sound_start_time = pygame.time.get_ticks()
        elif self.level != 5:
            self.level5_sound_played = False
            # Resume default background music if not already playing
            if not pygame.mixer.music.get_busy():
                self.play_menu_music()

        # Play level start sound
        if 'level_start' in self.assets.sounds:
            self.assets.sounds['level_start'].play()

    def spawn_enemy(self):
        if self.enemies_remaining <= 0:
            return

        # Get the chicken type for current level
        chicken_type_key = self.chicken_type_keys[min(
            self.level - 1, len(self.chicken_type_keys) - 1)]
        chicken_type = self.chicken_types[chicken_type_key]

        enemy = Enemy(self.assets, chicken_type, self)

        # Set spawn position within visible screen bounds
        enemy.rect.x = random.randrange(
            0, self.screen_width - enemy.rect.width)
        enemy.rect.y = random.randrange(-150, -50)  # Spawn above visible area

        # Scale enemy stats based on level
        enemy.health = int(enemy.health * (1 + (self.level - 1) * 0.1))
        enemy.speedy = int(enemy.speedy * (1 + (self.level - 1) * 0.05))
        enemy.points = int(enemy.points * (1 + (self.level - 1) * 0.1))

        self.all_sprites.add(enemy)
        self.enemies_group.add(enemy)
        self.enemies_remaining -= 1

    def check_level_complete(self):
        # Check if all enemies are defeated & Check if all Chickens Killed or not
        if len(self.enemies_group) == 0 and self.enemies_remaining == 0:
            if not self.level_complete:
                self.level_complete = True
                if self.level < self.max_levels:
                    self.level += 1
                    self.difficulty += 0.5
                    self.enemy_spawn_rate = max(
                        500, self.enemy_spawn_rate - 50)
                    self.state = LEVEL_TRANSITION

                    # Play level complete sound
                    if 'level_complete' in self.assets.sounds:
                        self.assets.sounds['level_complete'].play()
                else:
                    self.game_over(win=True)

    def draw_hud(self):
        # Health bar
        health_width = 200 * (self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(self.screen, GREEN, (10, 10, health_width, 20))

        # Score
        score_text = self.assets.fonts['small'].render(
            f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 40))

        # Level and Enemy Info
        chicken_type_key = self.chicken_type_keys[min(
            self.level - 1, len(self.chicken_type_keys) - 1)]
        chicken_type = self.chicken_types[chicken_type_key]

        level_text = self.assets.fonts['small'].render(
            f"Level {self.level}: {chicken_type.name}", True, WHITE)
        self.screen.blit(level_text, (10, 70))

        enemies_text = self.assets.fonts['small'].render(
            f"Enemies Remaining: {len(self.enemies_group) + self.enemies_remaining}", True, WHITE)
        self.screen.blit(enemies_text, (10, 100))

        # Lives
        for i in range(self.player.lives):
            self.screen.blit(self.assets.images['heart'], (10 + i * 30, 130))

        # Missiles
        missile_text = self.assets.fonts['small'].render(
            f"Missiles: {self.player.missiles}", True, WHITE)
        self.screen.blit(missile_text, (self.screen_width - 150, 10))

    def draw_level_transition(self):
        self.screen.blit(self.assets.images['background_blurred'], (0, 0))

        # Get next level's chicken type
        next_level = min(self.level, len(self.chicken_type_keys))
        chicken_type = self.chicken_types[self.chicken_type_keys[next_level - 1]]

        title = self.assets.fonts['large'].render(
            f"LEVEL {self.level} COMPLETE!", True, WHITE)
        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 100))

        next_enemy = self.assets.fonts['medium'].render(
            f"Next Enemy: {chicken_type.name}", True, WHITE)
        self.screen.blit(next_enemy, (self.screen_width //
                         2 - next_enemy.get_width()//2, 200))

        if chicken_type.special_ability:
            ability_text = self.assets.fonts['small'].render(
                f"Special Ability: {chicken_type.special_ability}", True, YELLOW)
            self.screen.blit(ability_text, (self.screen_width //
                             2 - ability_text.get_width()//2, 250))

        score_text = self.assets.fonts['medium'].render(
            f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (self.screen_width //
                         2 - score_text.get_width()//2, 300))

        self.next_button.draw(self.screen)
        self.shop_button.draw(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        self.next_button.check_hover(mouse_pos)
        self.shop_button.check_hover(mouse_pos)

    def new_game(self):  # start from scratch
        # Reset game state
        self.level = 1
        self.difficulty = 1
        self.enemy_spawn_rate = 1000  # time between the display of enemies

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()  # Add particles group

        # Create player
        self.player = Player(self.assets, self)
        self.all_sprites.add(self.player)

        # Start first level
        self.start_level()

        # Set game state
        self.state = PLAYING

        # Start music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        mixer.music.play(-1)  # Loop music indefinitely

    def check_collisions(self):  # Check the collisions between enemies and bullets
        hits = pygame.sprite.groupcollide(
            self.enemies_group, self.bullets, False, True)
        for enemy, bullets in hits.items():
            for bullet in bullets:
                enemy.health -= bullet.damage
                if enemy.health <= 0:
                    enemy.kill()
                    self.player.add_score(enemy.points)
                    expl = Explosion(enemy.rect.center, 'large', self.assets)
                    self.all_sprites.add(expl)
                    self.explosions.add(expl)
                    self.assets.sounds['explosion'].play()

                    if random.random() < 0.2:
                        self.spawn_powerup(enemy.rect.center)

        hits = pygame.sprite.groupcollide(
            self.enemies_group, self.missiles, False, True)
        for enemy, missiles in hits.items():
            for missile in missiles:
                enemy.health -= missile.damage
                if enemy.health <= 0:
                    enemy.kill()
                    self.player.add_score(enemy.points)
                    expl = Explosion(enemy.rect.center, 'large', self.assets)
                    self.all_sprites.add(expl)
                    self.explosions.add(expl)
                    self.assets.sounds['explosion'].play()

                    if random.random() < 0.3:
                        self.spawn_powerup(enemy.rect.center)

        hits = pygame.sprite.spritecollide(
            self.player, self.enemies_group, True, pygame.sprite.collide_mask)
        for enemy in hits:
            is_dead = self.player.take_damage(enemy.damage)
            expl = Explosion(enemy.rect.center, 'small', self.assets)
            self.all_sprites.add(expl)
            self.explosions.add(expl)
            self.assets.sounds['explosion'].play()

            if is_dead:
                self.game_over()

        hits = pygame.sprite.spritecollide(
            self.player, self.powerups, True, pygame.sprite.collide_mask)
        for powerup in hits:
            self.assets.sounds['powerup'].play()

            if powerup.type == 'health':
                self.player.health = min(
                    self.player.max_health, self.player.health + 25)
            elif powerup.type == 'power':
                self.player.powerup()
            elif powerup.type == 'missile':
                self.player.missiles += 1

    def spawn_powerup(self, center):
        power_types = ['health', 'power', 'missile']
        weights = [0.4, 0.4, 0.2]

        if self.player.health >= self.player.max_health * 0.8:
            weights[0] = 0.2
            weights[1] = 0.6

        if self.player.missiles >= 5:
            weights[2] = 0.1

        power_type = random.choices(power_types, weights=weights, k=1)[0]
        powerup = PowerUp(center, power_type, self.assets)
        self.all_sprites.add(powerup)
        self.powerups.add(powerup)

    def game_over(self, win=False):
        self.state = GAME_OVER
        # Update high scores before showing game over screen
        self.update_high_scores(self.player.score)

        if win and 'win' in self.assets.sounds:
            self.assets.sounds['win'].play()
        elif 'game_over' in self.assets.sounds:
            self.assets.sounds['game_over'].play()

    def update_high_scores(self, score):
        # Ensure we have a valid player name
        if not self.player_name:
            self.player_name = "Player"

        # Add new score with timestamp
        new_score = {
            "name": self.player_name,
            "score": score,
            "date": pygame.time.get_ticks()  # Add timestamp for sorting
        }

        # Add new score to the list
        self.high_scores.append(new_score)

        # Sort by score in descending order
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)

        # Keep only top 10 scores
        self.high_scores = self.high_scores[:10]

        # Save to file immediately
        self.save_high_scores()

    def save_high_scores(self):
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(self.high_scores, f, indent=4)
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as f:
                scores = json.load(f)
                # Convert old format (list of ints) to new format (list of dicts)
                if scores and isinstance(scores[0], (int, float)):
                    self.high_scores = [
                        {"name": f"Player{i+1}", "score": score,
                            "date": pygame.time.get_ticks()}
                        for i, score in enumerate(scores)
                    ]
                else:
                    self.high_scores = scores
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize with default scores if file doesn't exist
            self.high_scores = [
                {"name": "Player1", "score": 5000,
                    "date": pygame.time.get_ticks()},
                {"name": "Player2", "score": 3000,
                    "date": pygame.time.get_ticks()},
                {"name": "Player3", "score": 2000,
                    "date": pygame.time.get_ticks()},
                {"name": "Player4", "score": 1000,
                    "date": pygame.time.get_ticks()},
                {"name": "Player5", "score": 500, "date": pygame.time.get_ticks()}
            ]
            self.save_high_scores()

    def draw_menu(self):
        self.screen.blit(self.assets.images['background_blurred'], (0, 0))

        title = self.assets.fonts['large'].render("SPACE HUNTER", True, WHITE)
        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 100))

        for button in self.menu_buttons:
            button.draw(self.screen)

    def draw_high_scores(self):
        self.screen.blit(self.assets.images['background_blurred'], (0, 0))

        # Draw title with a nice background
        title_bg = pygame.Surface((400, 80), pygame.SRCALPHA)
        title_bg.fill((0, 0, 0, 180))
        title_rect = title_bg.get_rect(center=(self.screen_width//2, 80))
        self.screen.blit(title_bg, title_rect)

        title = self.assets.fonts['large'].render("HIGH SCORES", True, WHITE)
        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 50))

        # Draw scores with a nice background
        for i, entry in enumerate(self.high_scores[:10]):
            # Create a background for each score
            score_bg = pygame.Surface((500, 40), pygame.SRCALPHA)
            score_bg.fill((0, 0, 0, 150))
            score_rect = score_bg.get_rect(
                center=(self.screen_width//2, 180 + i * 50))
            self.screen.blit(score_bg, score_rect)

            # Draw rank with a different color
            rank_text = self.assets.fonts['medium'].render(
                f"{i+1}.", True, YELLOW)
            self.screen.blit(
                rank_text, (self.screen_width//2 - 220, 165 + i * 50))

            # Draw name and score
            name_text = self.assets.fonts['medium'].render(
                entry['name'], True, WHITE)
            score_text = self.assets.fonts['medium'].render(
                str(entry['score']), True, GREEN)

            # Add date if available
            if 'date' in entry:
                date = pygame.time.get_ticks() - entry['date']
                if date < 86400000:  # Less than 24 hours
                    time_text = "Today"
                elif date < 172800000:  # Less than 48 hours
                    time_text = "Yesterday"
                else:
                    time_text = f"{date // 86400000} days ago"
                date_surface = self.assets.fonts['small'].render(
                    time_text, True, (200, 200, 200))
                self.screen.blit(
                    date_surface, (self.screen_width//2 + 200, 165 + i * 50))

            self.screen.blit(
                name_text, (self.screen_width//2 - 180, 165 + i * 50))
            self.screen.blit(
                score_text, (self.screen_width//2 + 100, 165 + i * 50))

        # Draw back button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.screen)

    def draw_pause_screen(self):
        s = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))

        pause_text = self.assets.fonts['large'].render("PAUSED", True, WHITE)
        self.screen.blit(pause_text, (self.screen_width//2 -
                         pause_text.get_width()//2, self.screen_height//2 - 100))

        self.pause_button.draw(self.screen)
        self.back_button.draw(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        self.pause_button.check_hover(mouse_pos)
        self.back_button.check_hover(mouse_pos)

    def draw_game_over(self, win=False):
        self.screen.blit(self.assets.images['background_blurred'], (0, 0))

        if win:
            title = self.assets.fonts['large'].render("YOU WIN!", True, GREEN)
        else:
            title = self.assets.fonts['large'].render("GAME OVER", True, RED)

        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 100))

        score_text = self.assets.fonts['medium'].render(
            f"Final Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (self.screen_width //
                         2 - score_text.get_width()//2, 200))

        self.restart_button.draw(self.screen)
        self.menu_button.draw(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        self.restart_button.check_hover(mouse_pos)
        self.menu_button.check_hover(mouse_pos)

    def draw_settings_screen(self):
        self.screen.fill(BLACK)
        title = self.assets.fonts['large'].render("SETTINGS", True, WHITE)
        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 40))
        # Fire selection
        fire_label = self.assets.fonts['medium'].render(
            "Select Fire:", True, YELLOW)
        self.screen.blit(fire_label, (100, 120))
        for i, fname in enumerate(self.fire_options):
            img = pygame.image.load(os.path.join(
                'Images', 'Objects', 'Fire', fname)).convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            x = 100 + i*80
            y = 170
            rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, rect)
            if fname == self.selected_fire:
                pygame.draw.rect(self.screen, GREEN, rect, 3)
            # Store clickable rects for event handling
            if not hasattr(self, 'fire_rects'):
                self.fire_rects = []
            if len(self.fire_rects) <= i:
                self.fire_rects.append(rect)
            else:
                self.fire_rects[i] = rect
        # Spacecraft selection
        sc_label = self.assets.fonts['medium'].render(
            "Select Spacecraft:", True, YELLOW)
        self.screen.blit(sc_label, (100, 270))
        for i, fname in enumerate(self.spacecraft_options):
            img = pygame.image.load(os.path.join(
                'Images', 'Objects', 'Spacecraft', fname)).convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            x = 100 + i*80
            y = 320
            rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, rect)
            if fname == self.selected_spacecraft:
                pygame.draw.rect(self.screen, GREEN, rect, 3)
            if not hasattr(self, 'spacecraft_rects'):
                self.spacecraft_rects = []
            if len(self.spacecraft_rects) <= i:
                self.spacecraft_rects.append(rect)
            else:
                self.spacecraft_rects[i] = rect
        # Missile selection
        missile_label = self.assets.fonts['medium'].render(
            "Select Missile:", True, YELLOW)
        self.screen.blit(missile_label, (100, 420))
        for i, fname in enumerate(self.missile_options):
            img = pygame.image.load(os.path.join(
                'Images', 'Objects', 'Missile', fname)).convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            x = 100 + i*80
            y = 470
            rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, rect)
            if fname == self.selected_missile:
                pygame.draw.rect(self.screen, GREEN, rect, 3)
            if not hasattr(self, 'missile_rects'):
                self.missile_rects = []
            if len(self.missile_rects) <= i:
                self.missile_rects.append(rect)
            else:
                self.missile_rects[i] = rect
        # Back button
        if not hasattr(self, 'settings_back_button'):
            self.settings_back_button = Button(
                self.screen_width//2 - 100, self.screen_height - 100, 200, 50, "Back", BLUE, YELLOW)
        self.settings_back_button.draw(self.screen)

    def draw_name_input(self):
        self.screen.blit(self.assets.images['background_blurred'], (0, 0))

        title = self.assets.fonts['large'].render(
            "ENTER YOUR NAME", True, WHITE)
        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 100))

        # Draw input box
        input_box = pygame.Rect(self.screen_width//2 -
                                200, self.screen_height//2 - 25, 400, 50)
        pygame.draw.rect(self.screen, WHITE, input_box, 2)

        # Draw current name
        name_surface = self.assets.fonts['medium'].render(
            self.player_name, True, WHITE)
        self.screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # Draw continue button
        continue_button = Button(self.screen_width//2 - 100, self.screen_height//2 + 50,
                                 200, 50, "Continue", GREEN, YELLOW)
        continue_button.draw(self.screen)

        return continue_button

    def draw_about_screen(self):
        self.screen.blit(self.assets.images['background_blurred'], (0, 0))

        # Draw title
        title = self.assets.fonts['large'].render("ABOUT", True, WHITE)
        self.screen.blit(title, (self.screen_width //
                         2 - title.get_width()//2, 50))

        # Game description
        desc_lines = [
            "Chicken Invaders is a browser-based arcade game where players",
            "pilot a spaceship to fend off waves of invading chickens.",
            "Players can collect gifts, dodge obstacles, and progress through",
            "multiple stages, including early levels, a chicken matrix phase,",
            "an intense egg rain, and a final boss battle.",
            "",
            "This Game Has Been Created With <3 To Everybody.",
            "© 2025 Zer0Day Team. All rights reserved."
        ]

        y_offset = 120
        for line in desc_lines:
            text = self.assets.fonts['small'].render(line, True, WHITE)
            self.screen.blit(text, (self.screen_width//2 -
                             text.get_width()//2, y_offset))
            y_offset += 30

        # Development Team section
        team_title = self.assets.fonts['medium'].render(
            "Development Team", True, YELLOW)
        self.screen.blit(team_title, (self.screen_width//2 -
                         team_title.get_width()//2, y_offset + 20))

        # Team members
        team_members = [
            ("Team Leader", "Moataz Mahmoud", "42210055", "B2"),
            ("Team Member", "Adel Adel Ahmed", "42210211", "A2"),
            ("Team Member", "Ahmed Haytham", "42210126", "B2"),
            ("Team Member", "Abdelrahman Ahmed", "42210259", "A1"),
            ("Team Member", "Mohamed Abdel Fattah", "42210180", "B2"),
            ("Team Member", "Ahmed Farhat", "42210249", "A1")
        ]

        y_offset += 70
        for role, name, id, group in team_members:
            member_text = self.assets.fonts['small'].render(
                f"{role}: {name} (ID: {id}, Group: {group})", True, WHITE)
            self.screen.blit(member_text, (self.screen_width //
                             2 - member_text.get_width()//2, y_offset))
            y_offset += 30

        # Instructor
        instructor_text = self.assets.fonts['medium'].render(
            "Instructor: Eng. Diana Emad", True, YELLOW)
        self.screen.blit(instructor_text, (self.screen_width //
                         2 - instructor_text.get_width()//2, y_offset + 20))

        # Back button
        self.back_button.draw(self.screen)

    def run(self):
        last_enemy_spawn = pygame.time.get_ticks()
        while self.running:
            self.clock.tick(FPS)

            # Check if level 5 sound has finished
            if self.level == 5 and self.level5_sound_played:
                current_time = pygame.time.get_ticks()
                if current_time - self.level5_sound_start_time >= self.level5_sound_duration:
                    # Stop level 5 sound
                    if self.level5_sound:
                        self.level5_sound.stop()
                    # Resume default background music
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load('Sounds/Epic Hip Hop.wav')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                    self.level5_sound_played = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == NAME_INPUT:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.player_name:
                            self.state = MENU
                            self.play_menu_music()
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif len(self.player_name) < 15:  # Limit name length
                            self.player_name += event.unicode

                    mouse_pos = pygame.mouse.get_pos()
                    continue_button = self.draw_name_input()
                    continue_button.check_hover(mouse_pos)
                    if continue_button.is_clicked(mouse_pos, event) and self.player_name:
                        self.state = MENU
                        self.play_menu_music()

                elif self.state == INTRO:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.stop_all_sounds()
                        self.state = NAME_INPUT
                        self.intro_played = True
                        self.play_menu_music()  # Start menu music after intro

                elif self.state == PLAYING:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.shoot()
                        elif event.key == pygame.K_m:
                            self.player.shoot_missile()
                        elif event.key == pygame.K_p:
                            self.previous_state = PLAYING
                            self.state = SHOP
                        elif event.key == pygame.K_ESCAPE:
                            self.state = PAUSED
                            if 'pause' in self.assets.sounds:
                                self.assets.sounds['pause'].play()
                            self.stop_all_sounds()  # Stop all sounds when pausing
                            self.play_menu_music()  # Play menu music during pause
                        elif event.key == pygame.K_F11:  # Toggle fullscreen
                            if self.screen.get_flags() & pygame.FULLSCREEN:
                                self.screen = pygame.display.set_mode(
                                    (800, 900))
                            else:
                                self.screen = pygame.display.set_mode(
                                    (0, 0), pygame.FULLSCREEN)
                            self.screen_width, self.screen_height = self.screen.get_size()
                            self.assets.screen_width = self.screen_width
                            self.assets.screen_height = self.screen_height
                            self.assets.load_assets()
                            self.create_menu_buttons()

                elif self.state == PAUSED:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = PLAYING
                            if 'unpause' in self.assets.sounds:
                                self.assets.sounds['unpause'].play()
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_button.is_clicked(mouse_pos, event):
                            self.state = PLAYING
                            if 'unpause' in self.assets.sounds:
                                self.assets.sounds['unpause'].play()
                        elif self.back_button.is_clicked(mouse_pos, event):
                            self.state = MENU
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()
                    # Play default menu music if not already playing
                    try:
                        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                            pygame.mixer.music.load('Sounds/Epic Hip Hop.wav')
                            pygame.mixer.music.play(-1)
                    except Exception as e:
                        print(f"Menu music error: {e}")

                elif self.state == MENU:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.menu_buttons:
                        button.check_hover(mouse_pos)
                        if button.is_clicked(mouse_pos, event):
                            if button == self.start_button:
                                self.new_game()
                                if 'select' in self.assets.sounds:
                                    self.assets.sounds['select'].play()
                            elif button == self.high_scores_button:
                                self.state = HIGH_SCORES
                                if 'select' in self.assets.sounds:
                                    self.assets.sounds['select'].play()
                            elif button == self.about_button:  # New About button handler
                                self.state = ABOUT
                                if 'select' in self.assets.sounds:
                                    self.assets.sounds['select'].play()
                            elif button == self.quit_button:
                                self.running = False
                            elif button == self.settings_button:
                                self.state = SETTINGS

                elif self.state == HIGH_SCORES:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.back_button.is_clicked(mouse_pos, event):
                            self.state = MENU
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()

                elif self.state == SHOP:
                    result = self.shop.handle_event(event, self.player)
                    if result == 'back':
                        # Return to previous state
                        self.state = self.previous_state if self.previous_state else PLAYING
                        self.previous_state = None
                        if 'select' in self.assets.sounds:
                            self.assets.sounds['select'].play()
                    elif result == 'purchase':
                        # Show purchase message and return to previous state
                        self.shop_message = 'Purchase successful!'
                        self.shop_message_time = pygame.time.get_ticks()
                        if 'powerup' in self.assets.sounds:
                            self.assets.sounds['powerup'].play()
                        self.state = self.previous_state if self.previous_state else PLAYING
                        self.previous_state = None
                    elif result == 'fail':
                        self.shop_message = 'Not enough points!'
                        self.shop_message_time = pygame.time.get_ticks()
                        if 'hit' in self.assets.sounds:
                            self.assets.sounds['hit'].play()

                elif self.state == LEVEL_TRANSITION:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.next_button.is_clicked(mouse_pos, event):
                            self.state = PLAYING
                            self.start_level()
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()
                        elif self.shop_button.is_clicked(mouse_pos, event):
                            self.previous_state = LEVEL_TRANSITION
                            self.state = SHOP
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()

                elif self.state == GAME_OVER:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.restart_button.is_clicked(mouse_pos, event):
                            self.new_game()
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()
                        elif self.menu_button.is_clicked(mouse_pos, event):
                            self.state = MENU
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()

                elif self.state == SETTINGS:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Fire selection
                        for i, rect in enumerate(self.fire_rects):
                            if rect.collidepoint(mouse_pos):
                                self.selected_fire = self.fire_options[i]
                        # Spacecraft selection
                        for i, rect in enumerate(self.spacecraft_rects):
                            if rect.collidepoint(mouse_pos):
                                self.selected_spacecraft = self.spacecraft_options[i]
                        # Missile selection
                        for i, rect in enumerate(self.missile_rects):
                            if rect.collidepoint(mouse_pos):
                                self.selected_missile = self.missile_options[i]
                        # Back button
                        if self.settings_back_button.is_clicked(mouse_pos, event):
                            self.state = MENU
                    self.settings_back_button.check_hover(mouse_pos)

                elif self.state == ABOUT:  # New About state handler
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.back_button.is_clicked(mouse_pos, event):
                            self.state = MENU
                            if 'select' in self.assets.sounds:
                                self.assets.sounds['select'].play()

            # Update game state
            if self.state == PLAYING:
                now = pygame.time.get_ticks()
                if now - last_enemy_spawn > self.enemy_spawn_rate and self.enemies_remaining > 0:
                    self.spawn_enemy()
                    last_enemy_spawn = now

                self.all_sprites.update()
                self.check_collisions()
                self.check_level_complete()

            # Draw everything
            self.screen.blit(self.assets.images['background'], (0, 0))

            if self.state == PLAYING:
                self.all_sprites.draw(self.screen)
                self.draw_hud()
            elif self.state == PAUSED:
                self.all_sprites.draw(self.screen)
                self.draw_hud()
                self.draw_pause_screen()
            elif self.state == MENU:
                self.draw_menu()
            elif self.state == HIGH_SCORES:
                self.draw_high_scores()
            elif self.state == ABOUT:  # New About state drawing
                self.draw_about_screen()
            elif self.state == LEVEL_TRANSITION:
                self.draw_level_transition()
            elif self.state == GAME_OVER:
                self.draw_game_over()
            elif self.state == SHOP:
                self.all_sprites.draw(self.screen)
                self.draw_hud()
                self.shop.draw(self.screen, self.player.score)
            elif self.state == SETTINGS:
                self.draw_settings_screen()
            elif self.state == NAME_INPUT:
                self.draw_name_input()

            # Show shop message if any
            if self.shop_message and pygame.time.get_ticks() - self.shop_message_time < 1500:
                msg_surface = self.assets.fonts['medium'].render(
                    self.shop_message, True, YELLOW)
                self.screen.blit(
                    msg_surface, (self.screen_width//2 - msg_surface.get_width()//2, 60))
            elif self.shop_message and pygame.time.get_ticks() - self.shop_message_time >= 1500:
                self.shop_message = ''

            if self.state == INTRO:
                self.screen.fill(BLACK)
                # Play intro sound once
                if not self.intro_sound_played and self.intro_sound:
                    self.intro_sound.play()
                    self.intro_sound_played = True

                # Animate GIF
                gif_rect = None
                if self.intro_frames:
                    frame_duration = 100  # ms per frame
                    now = pygame.time.get_ticks()
                    self.intro_frame_index = (
                        (now - self.intro_start_time) // frame_duration) % len(self.intro_frames)
                    frame = self.intro_frames[self.intro_frame_index]
                    gif_rect = frame.get_rect(
                        center=(self.screen_width//2, self.screen_height//2 - 60))
                    self.screen.blit(frame, gif_rect)
                # Draw intro text below GIF
                intro_line0 = "Welcome to Chicken Invaders"
                intro_line1 = "This Game Has Been Created With <3 To Everybody"
                intro_line2 = "Copy Right © 2025 Zer0Day Team"
                font_large = self.assets.fonts['large']
                font_medium = self.assets.fonts['medium']
                # Render surfaces
                line0_surface = font_large.render(
                    intro_line0, True, (255, 255, 0))
                line1_surface = font_large.render(
                    intro_line1, True, (255, 255, 255))
                line2_surface = font_medium.render(
                    intro_line2, True, (200, 200, 200))
                # Position below GIF or center if GIF not loaded
                if gif_rect:
                    y_base = gif_rect.bottom + 30
                else:
                    y_base = self.screen_height // 2 + 30
                line0_rect = line0_surface.get_rect(
                    center=(self.screen_width//2, y_base))
                line1_rect = line1_surface.get_rect(
                    center=(self.screen_width//2, y_base + 50))
                line2_rect = line2_surface.get_rect(
                    center=(self.screen_width//2, y_base + 100))
                self.screen.blit(line0_surface, line0_rect)
                self.screen.blit(line1_surface, line1_rect)
                self.screen.blit(line2_surface, line2_rect)
                # Auto-advance after duration
                if pygame.time.get_ticks() - self.intro_start_time > self.intro_duration:
                    self.state = MENU
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()

            pygame.display.flip()

        pygame.quit()


#!============== Just For logger  ===============
# logger = logging.getLogger('chicken_invaders')
# logger.setLevel(logging.DEBUG)
# Create file handler which logs even debug messages
# file_handler = logging.FileHandler('chicken_invaders.log')
# file_handler.setLevel(logging.DEBUG)
# Create console handler with a higher log level
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# Create formatter and add it to the handlers
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)
# Add the handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
# Example usage:
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')


class IceParticle(pygame.sprite.Sprite):
    def __init__(self, pos, assets):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill((200, 230, 255))
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(
            random.uniform(-2, 2), random.uniform(-2, 2))
        self.lifetime = random.randint(30, 60)
        self.alpha = 255
        self.assets = assets

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.lifetime -= 1
        self.alpha = int((self.lifetime / 60) * 255)
        self.image.set_alpha(self.alpha)
        if self.lifetime <= 0:
            self.kill()


# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
