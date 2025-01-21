import pygame
from const import *
from entity import Entity


class Enemy(Entity):

    def __init__(self,position, frames, groups, player, collision_sprites):

        super().__init__(groups)

        # Player
        self.player = player

        # Animation
        self.frames = frames
        self.frame = 0
        self.animation_speed = ENEMY_ANIMATION_SPEED

        # Sprites, Hitbox
        self.image = self.frames[self.frame]
        self.rect = self.image.get_frect(center=position)
        self.hitbox_rect = self.rect.inflate(ENEMY_HITBOX) # const.py

        # Collision
        self.collision_sprites = collision_sprites

        # Movement
        self.direction = pygame.Vector2(0, 0)
        self.speed = ENEMY_SPEED # const.py

    def move(self, delta_time):

        # Player position
        player_pos = pygame.Vector2(self.player.rect.center)

        # Enemy position
        enemy_pos = pygame.Vector2(self.rect.center)

        # Movement
        self.direction = (player_pos - enemy_pos).normalize()
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')

        # Hitbox
        self.rect.center = self.hitbox_rect.center

    def animate(self, delta_time):

        self.frame += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame) % len(self.frames)]

    def update(self, delta_time):

        self.move(delta_time)
        self.animate(delta_time)