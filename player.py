import pygame
from os.path import join
from const import *
from entity import Entity
from item import Sword


class Player(Entity):

    def __init__(self, position, groups, collision_sprites, interactables_sprites, enemy_sprites):

        super().__init__(groups)
        self.isPlayer = True

        self.render_priority = 0

        self.position = position

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
        self.attack_cooldown = 0.5  # Time between attacks
        self.last_attack_time = 0

        # Equip cooldown
        self.equip_cooldown = 0.5  # 500 ms cooldown for equipping items
        self.last_equip_time = 0  # Last time item was equipped


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
            # Create an attack hitbox based on the direction the player is facing
            attack_rect = pygame.Rect(self.rect.centerx, self.rect.centery, 50, 20)  # Adjust size as needed

            # Adjust attack area based on direction
            if self.state == 'up':
                attack_rect.center = self.rect.centerx, self.rect.top
                attack_rect.height = 30  # Adjust the size as needed
            elif self.state == 'down':
                attack_rect.center = self.rect.centerx, self.rect.bottom
                attack_rect.height = 30  # Adjust the size as needed
            elif self.state == 'left':
                attack_rect.center = self.rect.left, self.rect.centery
                attack_rect.width = 30  # Adjust the size as needed
            elif self.state == 'right':
                attack_rect.center = self.rect.right, self.rect.centery
                attack_rect.width = 30  # Adjust the size as needed

            # Check for collisions with enemies in the attack area
            for enemy in self.enemy_sprites:  # Assuming enemies are in group 1 (enemy_sprites)
                if attack_rect.colliderect(enemy.rect):
                    enemy.health -= self.equipped.damage  # Deal damage
                    print(f'{enemy.enemy_name} hit for {self.equipped.damage} damage!')


    def input(self):

        keys = pygame.key.get_pressed()

        # Attack input
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.last_attack_time > self.attack_cooldown * 1000:
            self.attack()
            self.last_attack_time = pygame.time.get_ticks()

        # Movement
        self.direction.x = int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction


    def interact(self):

        for obj in self.interactables_sprites:

            if self.is_facing_object(obj):
                obj.interact()  # Trigger interaction
                return  # Only interact with one object at a time

    def is_facing_object(self, obj):

        # Check proximity
        interaction_distance = 30  # Adjust as needed
        player_center = pygame.Vector2(self.hitbox_rect.center)
        object_center = pygame.Vector2(obj.rect.center)

        # Calculate distance between the centers
        distance = player_center - object_center

        # If the distance is too great, return False
        if distance.length() > interaction_distance:
            return False

        # Check if the player is facing the object
        if self.state == 'up' and distance.y > 0 and abs(distance.x) < interaction_distance:
            return True
        if self.state == 'down' and distance.y < 0 and abs(distance.x) < interaction_distance:
            return True
        if self.state == 'left' and distance.x > 0 and abs(distance.y) < interaction_distance:
            return True
        if self.state == 'right' and distance.x < 0 and abs(distance.y) < interaction_distance:
            return True

        # If none of the conditions are met, the player is not facing the object properly
        return False

    def check_health(self):

        if self.health <= 0:
            self.alive = False
            self.kill()

    def equip_item(self, item):
        current_time = pygame.time.get_ticks()

        # Equip only if cooldown has passed
        if current_time - self.last_equip_time > self.equip_cooldown * 1000:
            if item.equippable:
                # If item is already equipped, unequip it
                if self.equipped:
                    if self.equipped == item:  # Check if the same item is being unequipped
                        self.equipped.unequip(self)
                        self.equipped = None  # Clear equipped item
                        print(f"Unequipped {item.name}")
                        return  # Exit early if we're unequipping

                # Equip the item if not already equipped
                item.equip(self)
                self.equipped = item
                print(f"Equipped {item.name}")

            # Reset equip time after equipping or unequipping
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