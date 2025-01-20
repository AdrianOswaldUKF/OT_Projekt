import os

import pygame

from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, position, group, collision_sprites):

        super().__init__(group)

        # Sprite Dicts
        self.frames = {
            'left': [],
            'right': [],
            'up': [],
            'down': []
        }

        # Load Sprites
        self.state = 'down'
        self.frame = 0
        self.image = pygame.image.load(join('assets','sprites','player', self.state, '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=position)
        self.load_images()

        # Movement

        self.direction = pygame.Vector2(0, 0)
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):

        for state in self.frames.keys():
            for folder_path, sub_folders, files_names in os.walk(join('assets','sprites','player', state)):
                if files_names:
                    for file_name in sorted(files_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)

    def animate(self, delta):

        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'

        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame += (self.frame + 5) if self.direction else 0
        self.image = self.frames[self.state][int(self.frame) % len(self.frames[self.state])]

    def move(self, delta):

        self.rect.center += self.direction * delta * self.speed

    def input(self):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, delta):

        self.input()
        self.move(delta)
        self.animate(delta)