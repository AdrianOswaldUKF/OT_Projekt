from os.path import join
from random import randint

import pygame

from const import *
from entity import Entity


class Enemy(Entity):

    def __init__(self, name, position, groups, player, collision_sprites):

        super().__init__(groups)
        self.isEnemy = True

        self.render_priority = 1

        self.enemy_name = name

        # Sprites, Hitbox
        self.image = pygame.image.load(join('assets', 'sprites', 'enemies', name, '0.png')).convert_alpha()
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

        # Movement
        self.direction = pygame.Vector2()
        self.speed = 0

        # Random Movement
        self.move_time = 0      # Time to move for a certain period (in seconds)
        self.wait_time = 0      # Time to wait before moving again (in seconds)
        self.move_duration = 2  # How long to move (in seconds)
        self.wait_duration = 1  # How long to wait before changing direction (in seconds)
        self.is_waiting = False # Flag to check if the enemy is waiting

        # Health
        self.health = 0

        # Damage
        self.damage = 0
        self.damage_cooldown = 0.5
        self.last_damage = 0

    def load_images(self):

        for i in range(9):
            file_path = join('assets', 'sprites', 'enemies', self.enemy_name, f'{i}.png')
            if file_path:
                self.animation_sprites.append((pygame.image.load(file_path).convert_alpha()))

    def move(self, delta_time):

        # If player is alive
        if self.player.alive:
            player_pos, enemy_pos = pygame.Vector2(self.player.rect.center), pygame.Vector2(self.rect.center)
            direction_vector = player_pos - enemy_pos

            if direction_vector.length() != 0:
                self.direction = direction_vector.normalize()
            else:
                self.direction = pygame.Vector2()

        # Wait
        elif self.is_waiting:
            self.wait_time -= delta_time

            if self.wait_time <= 0:
                self.is_waiting = False
                self.move_time = self.move_duration
                self.wait_time = self.wait_duration

        # If player is not alive
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

        # Horizontal Movement
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        # Vertical Movement
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')

        # Center hitbox
        self.rect.center = self.hitbox_rect.center

    def animate(self, delta_time):

        self.frame += self.animation_speed * delta_time
        self.image = self.animation_sprites[int(self.frame) % len(self.animation_sprites)]
        self.image = pygame.transform.scale(self.image, SLIME_SIZE) # const.py


    def update(self, delta_time):

        self.move(delta_time)
        self.animate(delta_time)


    def deal_damage(self, delta_time):

        if not self.player.alive:
            return

        self.last_damage += delta_time

        if not self.last_damage >= self.damage_cooldown:
            return

        self.player.health -= self.damage
        self.last_damage = 0

class Slime(Enemy):

    def __init__(self, position, groups, player, collision_sprites):

        super().__init__('slime', position, groups, player, collision_sprites)

        self.image = pygame.transform.scale(self.image, SLIME_SIZE)  # const.py
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX) # const.py

        self.animation_speed = SLIME_ANIMATION_SPEED
        self.speed = SLIME_SPEED  # const.py

        # HP
        self.health = 20

        # Damage
        self.damage = 5