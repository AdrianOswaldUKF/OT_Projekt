import pygame
from os.path import join
from const import *
from entity import Entity

class Enemy(Entity):

    def __init__(self, groups, player, collision_sprites):

        super().__init__(groups)

        # Player
        self.player = player

        # Animation
        self.frame = 0

        # Collision
        self.collision_sprites = collision_sprites

        # Movement
        self.direction = pygame.Vector2()

        self.speed = 0

    def move(self, delta_time):

        # Player position
        player_pos = pygame.Vector2(self.player.rect.center)

        # Enemy position
        enemy_pos = pygame.Vector2(self.rect.center)

        # Movement
        self.direction = (player_pos - enemy_pos).normalize()

        # Horizontal Movement
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        # Vertical Movement
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')

        # Hitbox
        self.rect.center = self.hitbox_rect.center

    def animate(self, delta_time):

        pass
        #self.frame += self.animation_speed * delta_time
        #self.image = self.frames[int(self.frame) % len(self.frames)]

    def update(self, delta_time):

        self.move(delta_time)
        self.animate(delta_time)

class Slime(Enemy):

    def __init__(self, position, groups, player, collision_sprites):

        super().__init__(groups, player, collision_sprites)

        # Sprites, Hitbox
        self.image = pygame.image.load(join('assets', 'sprites', 'enemies', 'slime', '0.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, SLIME_SIZE)  # const.py
        self.rect = self.image.get_frect(center=position)
        self.hitbox_rect = self.rect.inflate(SLIME_HITBOX) # const.py

        self.animation_speed = SLIME_ANIMATION_SPEED
        self.speed = SLIME_SPEED  # const.py