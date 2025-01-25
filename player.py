import pygame
from os.path import join
from const import *
from entity import Entity


class Player(Entity):

    def __init__(self, position, groups, collision_sprites):

        super().__init__(groups)
        self.isPlayer = True

        self.render_priority = 0

        # Static sprites
        self.static_sprites = {
            'up': '',
            'down': '',
            'left': '',
            'right': ''
        }

        # Animation sprites
        self.animation_sprites = {
            'up': [],
            'down': [],
            'left': [],
            'right': []
        }

        # Animation
        self.state = 'down'
        self.frame = 0

        # Sprites
        self.image = pygame.image.load(join('assets','sprites','player', 'player_down.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE) # const.py
        self.rect = self.image.get_frect(center=position)
        self.hitbox_rect = self.rect.inflate(PLAYER_HITBOX) # const.py

        # Load images into dictionaries
        self.load_images()

        # Movement
        self.direction = pygame.Vector2()
        self.speed = PLAYER_SPEED # const.py
        self.collision_sprites = collision_sprites

        # Health
        self.health = 100

        # Equipped Item
        self.equipped = None

        # Inventory
        self.inventory = []

    def load_images(self):

        for state in self.static_sprites.keys():
            file_path = join('assets', 'sprites', 'player', f'player_{state}.png')
            if file_path:
                self.static_sprites[state] = (pygame.image.load(file_path).convert_alpha())

        for state in self.animation_sprites.keys():
            for i in range(1, 3):
                file_path = join('assets', 'sprites', 'player', f'player_{state}{i}.png')
                if file_path:
                    self.animation_sprites[state].append(pygame.image.load(file_path).convert_alpha())

    def animate(self, delta_time):

        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'

        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        if self.direction:
            self.frame += 5 * delta_time
            self.image = self.animation_sprites[self.state][int(self.frame) % len(self.animation_sprites[self.state])]
            self.image = pygame.transform.scale(self.image, PLAYER_SIZE) # const.py
        else:
            self.image = self.static_sprites[self.state]
            self.image = pygame.transform.scale(self.image, PLAYER_SIZE) # const.py

    def move(self, delta_time):

        # Horizontal Movement
        self.hitbox_rect.x += self.direction.x * delta_time * self.speed
        self.collision('horizontal')

        # Vertical Movement
        self.hitbox_rect.y += self.direction.y * delta_time * self.speed
        self.collision('vertical')

        # Center hitbox
        self.rect.center = self.hitbox_rect.center

    def input(self):

        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def check_health(self):
        if self.health <= 0:
            self.alive = False
            self.kill()

    def update(self, delta_time):

        self.input()
        self.move(delta_time)
        self.animate(delta_time)
        self.check_health()