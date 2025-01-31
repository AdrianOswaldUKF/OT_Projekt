import pygame
from os.path import join
from const import *
from entity import Entity
from slash import Slash
from sword import Sword


class Player(Entity):

    def __init__(self, position, groups, collision_sprites, interactables_sprites, enemy_sprites):

        super().__init__(groups)
        self.isPlayer = True

        self.render_priority = 0

        self.position = position
        self.groups = groups

        self.interactables_sprites = interactables_sprites
        self.enemy_sprites = enemy_sprites

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
        self.inventory_open = False
        self.inventory_ui = None

        # Attacking
        self.attack_rect = pygame.Rect(self.rect.centerx, self.rect.centery, PLAYER_ATTACK_WIDTH, PLAYER_ATTACK_HEIGHT)
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.last_attack_time = 0

        self.is_attacking = False
        self.slash = None

        self.attack_sounds = [
            pygame.mixer.Sound(join('assets', 'sounds', 'player', 'slash', '0.wav')),
            pygame.mixer.Sound(join('assets', 'sounds', 'player', 'slash', '1.wav'))
        ]
        self.attack_count = 0

        # Equip cooldown
        self.equip_cooldown = PLAYER_EQUIP_COOLDOWN
        self.last_equip_time = 0

        self.equip_sound = pygame.mixer.Sound(join('assets', 'sounds', 'player', 'equip', '0.wav'))
        self.unequip_sound = pygame.mixer.Sound(join('assets', 'sounds', 'player', 'unequip', '0.wav'))


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

    def attack(self):

        if self.equipped and isinstance(self.equipped, Sword):

            # Attack based on direction
            if self.state == 'up':

                self.attack_rect.center = (self.rect.centerx, self.rect.top - 15)
                self.attack_rect.height = 50

            elif self.state == 'down':

                self.attack_rect.center = (self.rect.centerx, self.rect.bottom + 15)
                self.attack_rect.height = 50

            elif self.state == 'left':

                self.attack_rect.center = (self.rect.left - 20, self.rect.centery)
                self.attack_rect.width = 50

            elif self.state == 'right':

                self.attack_rect.center = (self.rect.right + 25, self.rect.centery)
                self.attack_rect.width = 50

            self.slash = Slash(self.attack_rect, self.attack_rect.center, self.direction, self.equipped.name, self.groups)
            self.is_attacking = False

            self.equipped.attack(self.attack_rect, self, self.enemy_sprites)

            sound_to_play = self.attack_sounds[self.attack_count % len(self.attack_sounds)]
            sound_to_play.play()

            self.attack_count += 1

    def input(self):

        keys = pygame.key.get_pressed()

        # Attack input
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.last_attack_time > self.attack_cooldown * 1000:

            self.attack()
            self.last_attack_time = pygame.time.get_ticks()

        # Movement
        self.direction.x = ((keys[pygame.K_d] - keys[pygame.K_a]) + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])) * self.speed
        self.direction.y = ((keys[pygame.K_s] - keys[pygame.K_w]) + (keys[pygame.K_DOWN] - keys[pygame.K_UP])) * self.speed
        self.direction = self.direction.normalize() if self.direction.length() > 0 else self.direction

    def interact(self):

        for obj in self.interactables_sprites:

            if self.is_facing_object(obj):

                obj.interact()
                return

    def is_facing_object(self, obj):

        interaction_distance = PLAYER_INTERACTION_DISTANCE
        player_center = pygame.Vector2(self.hitbox_rect.center)
        object_center = pygame.Vector2(obj.rect.center)


        distance = player_center - object_center


        if distance.length() > interaction_distance:

            return False


        if self.state == 'up' and distance.y > 0 and abs(distance.x) < interaction_distance:

            return True
        if self.state == 'down' and distance.y < 0 and abs(distance.x) < interaction_distance:

            return True
        if self.state == 'left' and distance.x > 0 and abs(distance.y) < interaction_distance:

            return True
        if self.state == 'right' and distance.x < 0 and abs(distance.y) < interaction_distance:

            return True


        return False

    def check_health(self):

        if self.health <= 0:

            self.alive = False
            self.kill()

    def heal(self, amount):

        self.health = min(self.health + amount, 100)

    def handle_item_switch(self):

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        for i in range(1, 6):

            if keys[getattr(pygame, f'K_{i}')]:

                item_index = i - 1

                if 0 <= item_index < len(self.inventory):

                    if current_time - self.last_equip_time >= self.equip_cooldown:

                        selected_item = self.inventory[item_index]
                        self.equip_item(selected_item)
                        self.last_equip_time = current_time

                    break

    def equip_item(self, item):

        current_time = pygame.time.get_ticks()

        if current_time - self.last_equip_time > self.equip_cooldown * 1000:

            if item.equippable:

                if self.equipped:

                     if self.equipped == item:
                         pass
                    #
                    #     self.equipped.unequip(self)
                    #     self.equipped = None
                    #     self.unequip_sound.play()
                    #
                    #     return

                item.equip(self)
                self.equipped = item
                self.equip_sound.play()

            self.last_equip_time = current_time

    def toggle_inventory(self):

        self.inventory_open = not self.inventory_open

        if self.inventory_open and self.inventory_ui:

            self.inventory_ui.open(self.inventory)

        elif self.inventory_ui:

            self.inventory_ui.close()

    def update(self, delta_time):

        self.input()
        self.move(delta_time)
        self.animate(delta_time)
        self.check_health()