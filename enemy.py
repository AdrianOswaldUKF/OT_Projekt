import pygame
import random
import os
from random import randint, uniform
from const import *
from entity import Entity
from item import HealingPotion


class Enemy(Entity):

    def __init__(self, name, position, groups, player, collision_sprites, enemy_sprites, all_sprites):

        super().__init__(groups)
        self.isEnemy = True

        self.render_priority = 1

        self.enemy_name = name
        self.all_sprites = all_sprites

        self.position = position

        # Sprites, Hitbox
        self.image = pygame.image.load(os.path.join('assets', 'sprites', 'enemies', name, '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=position)

        # Animation sprites
        self.animation_sprites = []

        self.load_images()

        # Player
        self.player = player

        # Animation
        self.frame = 0
        self.animation_speed = 0

        # Collision
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites

        # Movement
        self.direction = pygame.Vector2()
        self.speed = 0
        self.chasing = False  # Whether the enemy is chasing the player

        # Line of Sight (LOS)
        self.los_size = ENEMY_LOS  # LOS dimensions (width, height)
        self.line_of_sight = pygame.Rect(0, 0, *self.los_size)

        # Random Movement
        self.move_time = 0      # Time to move for a certain period (in seconds)
        self.wait_time = 0      # Time to wait before moving again (in seconds)
        self.move_duration = 2  # How long to move (in seconds)
        self.wait_duration = 1  # How long to wait before changing direction (in seconds)
        self.is_waiting = False # Flag to check if the enemy is waiting

        # Health
        self.health = 1
        self.max_health = self.health

        # Damage
        self.damage = 0
        self.damage_cooldown = 0.5
        self.last_damage = 0

        # Element
        self.element = "None"

        # Burning Effect
        self.burning_sprites = []
        self.burn_frame = 0
        self.load_burning_images()

        # Status Effects
        self.burning = False
        self.burn_timer = 0
        self.total_burn_time = 0
        self.stunned = False
        self.stun_duration = 0

        # Knockback
        self.knockback = False
        self.knockback_duration = 0
        self.knockback_speed = 0

        self.hurt_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'enemy', 'hit', '0.wav'))
        self.hurt_sound.set_volume(0.5)

    def load_images(self):

        folder_path = os.path.join('assets', 'sprites', 'enemies', self.enemy_name)

        file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])

        for i in range(file_count-1):

            file_path = os.path.join('assets', 'sprites', 'enemies', self.enemy_name, f'{i}.png')

            if file_path:

                self.animation_sprites.append(pygame.image.load(file_path).convert_alpha())

    def load_burning_images(self):

        folder_path = os.path.join('assets', 'sprites', 'effects', 'fire')

        if os.path.exists(folder_path):

            file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])

            for i in range(file_count-1):

                file_path = os.path.join('assets', 'sprites', 'effects', 'fire', f'{i}.png')

                if file_path:

                    self.burning_sprites.append(pygame.image.load(file_path).convert_alpha())

    def update_los(self):

        self.line_of_sight.center = self.rect.center

    def apply_knockback(self, knockback_direction, knockback_speed, knockback_duration):

        self.knockback = True
        self.direction = knockback_direction
        self.knockback_speed = knockback_speed
        self.knockback_duration = knockback_duration

    def move(self, delta_time):

        if self.knockback:

            original_position = self.hitbox_rect.topleft

            self.hitbox_rect.x += self.direction.x * self.knockback_speed * delta_time
            if self.collision('horizontal'):

                self.hitbox_rect.x = original_position[0]
                self.direction.x = 0

            self.hitbox_rect.y += self.direction.y * self.knockback_speed * delta_time
            if self.collision('vertical'):

                self.hitbox_rect.y = original_position[1]
                self.direction.y = 0

            self.rect.center = self.hitbox_rect.center

            self.knockback_duration -= delta_time

            if self.knockback_duration <= 0:

                self.knockback = False

            return

        if self.stunned:

            return

        self.update_los()

        if self.line_of_sight.colliderect(self.player.rect):

            self.chasing = True
        else:

            self.chasing = False

        if self.chasing and self.player.alive:

            player_pos = pygame.Vector2(self.player.rect.center)
            enemy_pos = pygame.Vector2(self.rect.center)
            direction_vector = player_pos - enemy_pos

            if direction_vector.length() != 0:

                self.direction = direction_vector.normalize()
            else:

                self.direction = pygame.Vector2()

            for enemy in self.enemy_sprites:
                if enemy != self:

                    distance = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center)
                    if distance.length() < ENEMY_DISTANCE_THRESHOLD:

                        if distance.length() != 0:

                            self.direction += distance.normalize() * 0.5

        elif self.is_waiting:

            self.wait_time -= delta_time
            if self.wait_time <= 0:

                self.is_waiting = False
                self.move_time = self.move_duration

        else:

            self.move_time -= delta_time
            if self.move_time <= 0:

                self.is_waiting = True
                random_direction = pygame.Vector2(randint(-1, 1), randint(-1, 1))

                if random_direction.length() != 0:

                    self.direction = random_direction.normalize()
                else:

                    self.direction = pygame.Vector2()

                self.wait_time = self.wait_duration


        original_position = self.hitbox_rect.topleft

        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        if self.collision('horizontal'):

            self.hitbox_rect.x = original_position[0]
            self.direction.x = 0

        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        if self.collision('vertical'):

            self.hitbox_rect.y = original_position[1]
            self.direction.y = 0

        self.rect.center = self.hitbox_rect.center

    def animate(self, delta_time):


        if self.stunned:

            self.burn_animation(delta_time)
            return

        self.frame += self.animation_speed * delta_time
        self.image = self.animation_sprites[int(self.frame) % len(self.animation_sprites)]
        self.image = pygame.transform.scale(self.image, self.rect.size)

        self.burn_animation(delta_time)

    def burn_animation(self, delta_time):

        if self.burning and self.burning_sprites:

            self.burn_frame += delta_time * 10
            burn_image = self.burning_sprites[int(self.burn_frame) % len(self.burning_sprites)]

            burn_image = pygame.transform.scale(burn_image, self.image.get_size())

            self.image.blit(burn_image, (0, 0))

    def drop_loot(self):
        drop_chance = 0.4

        if random.random() < drop_chance:
            HealingPotion(self.rect.centerx, self.rect.centery, self.player, self.all_sprites)

    def update(self, delta_time):

        self.move(delta_time)
        self.animate(delta_time)

        if self.health <= 0:

            self.drop_loot()
            self.alive = False
            self.kill()

            return

        if self.burning:

            self.burn_timer += delta_time

            if self.burn_timer >= 1:

                self.hurt_sound.play()
                self.health -= 5
                self.burn_timer = 0

            self.total_burn_time += delta_time

            if self.total_burn_time >= BURN_TIME:

                self.burning = False
                self.burn_frame = 0
                self.total_burn_time = 0

        else:
            self.total_burn_time = 0

        if self.stunned:

            self.stun_duration -= delta_time

            if self.stun_duration <= 0:
                self.stunned = False


    def deal_damage(self, delta_time):

        if not self.player.alive:

            return

        self.last_damage += delta_time
        if not self.last_damage >= self.damage_cooldown:

            return

        self.player.health -= self.damage
        self.last_damage = 0

    def render_health_bar(self, screen, offset):

        max_bar_width = SLIME_SIZE[0]
        bar_height = 5

        health_percentage = self.health / self.max_health
        bar_width = max_bar_width * health_percentage

        bar_x = self.rect.centerx - bar_width / 2
        bar_y = self.rect.top - 10
        bar_x += offset.x
        bar_y += offset.y

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, max_bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))


class Slime(Enemy):

    def __init__(self, position, groups, player, collision_sprites, enemy_sprites, all_sprites, scale_factor=None):

        super().__init__('slime', position, groups, player, collision_sprites, enemy_sprites, all_sprites)

        scale_factor = scale_factor if scale_factor else uniform(0.5, 1.5)

        self.size = (int(SLIME_SIZE[0] * scale_factor), int(SLIME_SIZE[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX[0] * scale_factor, SLIME_HITBOX[1] * scale_factor)

        # Stats
        if scale_factor < 1:
            self.speed = SLIME_SPEED * (1 / scale_factor)
        else:
            self.speed = SLIME_SPEED / scale_factor

        self.health = int(SLIME_HEALTH * scale_factor)
        self.max_health = self.health
        self.damage = int(SLIME_DAMAGE * scale_factor)

        # Animation
        self.animation_speed = SLIME_ANIMATION_SPEED



class WaterSlime(Enemy):

    def __init__(self, position, groups, player, collision_sprites, enemy_sprites, all_sprites, scale_factor=None):

        super().__init__('water_slime', position, groups, player, collision_sprites, enemy_sprites, all_sprites)

        scale_factor = scale_factor if scale_factor else uniform(0.5, 1.5)

        self.size = (int(SLIME_SIZE[0] * scale_factor), int(SLIME_SIZE[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX[0] * scale_factor, SLIME_HITBOX[1] * scale_factor)

        # Stats
        if scale_factor < 1:

            self.speed = SLIME_SPEED * (1 / scale_factor)
        else:

            self.speed = SLIME_SPEED / scale_factor

        self.health = int(WATER_SLIME_HEALTH * scale_factor)
        self.max_health = self.health
        self.damage = int(WATER_SLIME_DAMAGE * scale_factor)
        self.element = 'Water'

        # Animation
        self.animation_speed = SLIME_ANIMATION_SPEED

class FireSlime(Enemy):

    def __init__(self, position, groups, player, collision_sprites, enemy_sprites, all_sprites, scale_factor=None):

        super().__init__('fire_slime', position, groups, player, collision_sprites, enemy_sprites, all_sprites)

        scale_factor = scale_factor if scale_factor else uniform(0.5, 1.5)


        self.size = (int(SLIME_SIZE[0] * scale_factor), int(SLIME_SIZE[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX[0] * scale_factor, SLIME_HITBOX[1] * scale_factor)

        # Stats
        if scale_factor < 1:

            self.speed = SLIME_SPEED * (1 / scale_factor)
        else:

            self.speed = SLIME_SPEED / scale_factor

        self.health = int(FIRE_SLIME_HEALTH * scale_factor)
        self.max_health = self.health
        self.damage = int(FIRE_SLIME_DAMAGE * scale_factor)
        self.element = 'Fire'

        # Animation
        self.animation_speed = SLIME_ANIMATION_SPEED

        # Burning Effect
        self.burning_sprites = []
        self.burn_frame = 0
        self.load_burning_images()

    def load_burning_images(self):

        folder_path = os.path.join('assets', 'sprites', 'effects', 'fire')

        if os.path.exists(folder_path):

            file_count = len(
                [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])

            for i in range(file_count - 1):

                file_path = os.path.join('assets', 'sprites', 'effects', 'water_splash', f'{i}.png')

                if file_path:

                    self.burning_sprites.append(pygame.image.load(file_path).convert_alpha())

class EarthSlime(Enemy):

    def __init__(self, position, groups, player, collision_sprites, enemy_sprites, all_sprites, scale_factor=None):

        super().__init__('earth_slime', position, groups, player, collision_sprites, enemy_sprites, all_sprites)


        scale_factor = scale_factor if scale_factor else uniform(0.5, 1.5)


        self.size = (int(SLIME_SIZE[0] * scale_factor), int(SLIME_SIZE[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX[0] * scale_factor, SLIME_HITBOX[1] * scale_factor)

        # Stats
        if scale_factor < 1:

            self.speed = SLIME_SPEED * (1 / scale_factor)
        else:

            self.speed = SLIME_SPEED / scale_factor

        self.health = int(EARTH_SLIME_HEALTH * scale_factor)
        self.max_health = self.health
        self.damage = int(EARTH_SLIME_DAMAGE * scale_factor)
        self.element = 'Earth'

        # Animation
        self.animation_speed = SLIME_ANIMATION_SPEED

class AirSlime(Enemy):

    def __init__(self, position, groups, player, collision_sprites, enemy_sprites, all_sprites, scale_factor=None):

        super().__init__('air_slime', position, groups, player, collision_sprites, enemy_sprites, all_sprites)

        scale_factor = scale_factor if scale_factor else uniform(0.5, 1.5)


        self.size = (int(SLIME_SIZE[0] * scale_factor), int(SLIME_SIZE[1] * scale_factor))
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX[0] * scale_factor, SLIME_HITBOX[1] * scale_factor)

        # Stats
        if scale_factor < 1:

            self.speed = SLIME_SPEED * (1 / scale_factor)
        else:

            self.speed = SLIME_SPEED / scale_factor

        self.health = int(AIR_SLIME_HEALTH * scale_factor)
        self.max_health = self.health
        self.damage = int(AIR_SLIME_DAMAGE * scale_factor)
        self.element = 'Air'

        # Animation
        self.animation_speed = SLIME_ANIMATION_SPEED