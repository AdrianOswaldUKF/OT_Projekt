import pygame
import random
import os

from const import *
from damage_number import DamageNumber
from item import Item

class Sword(Item):
    def __init__(self, name, image, damage, element, attack_range=50, equippable=True):

        pygame.mixer.init()
        super().__init__(name, image, equippable)

        self.damage = damage
        self.attack_range = attack_range
        self.element = element
        self.knockback_speed = DEFAULT_KNOCKBACK_SPEED
        self.knockback_duration = DEFAULT_KNOCKBACK_DURATION

        self.damage_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'enemy' , 'hit','0.wav'))
        self.damage_sound.set_volume(0.5)


    def attack(self, attack_rect, player, enemies):

        if self.equipped:

            for enemy in enemies:

                if attack_rect.colliderect(enemy.rect):  # Check if enemy is within range

                    self.apply_effect(player, enemy)


    def apply_effect(self, player, enemy):

        self.damage_sound.play()

        enemy.health -= self.damage

        damage_sprite = DamageNumber(self.damage, enemy.rect.center)
        enemy.all_sprites.add(damage_sprite)

        knockback_force = pygame.Vector2(enemy.rect.center) - pygame.Vector2(player.rect.center)

        if knockback_force.length() != 0:

            knockback_direction = knockback_force.normalize()
            enemy.apply_knockback(knockback_direction, self.knockback_speed, self.knockback_duration)

# Basic Sword (No Special Effect)
class BasicSword(Sword):

    def __init__(self):

            super().__init__('Basic Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'basic', 'sword.png')), damage=10, element='None')

# Fire Sword (Burns Non-Fire Slimes)
class FireSword(Sword):

    def __init__(self):

        super().__init__('Fire Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'fire', 'sword.png')), damage=15, element='Fire')

    def apply_effect(self, player, enemy):

        if enemy.element == 'Fire':

            return

        bonus_damage = 10 if enemy.element != 'Fire' and enemy.element !='Water' else 0
        total_damage = self.damage + bonus_damage

        self.damage_sound.play()
        enemy.health -= total_damage

        damage_sprite = DamageNumber(total_damage, enemy.rect.center)
        enemy.all_sprites.add(damage_sprite)

        if enemy.element != 'Fire' and enemy.element !='Water':

            enemy.burning = True

        knockback_force = pygame.Vector2(enemy.rect.center) - pygame.Vector2(player.rect.center)

        if knockback_force.length() != 0:

            knockback_direction = knockback_force.normalize()
            enemy.apply_knockback(knockback_direction, self.knockback_speed, self.knockback_duration)

# Water Sword (Extra Damage to Fire Slimes)
class WaterSword(Sword):

    def __init__(self):

        super().__init__('Water Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'water', 'sword.png')), damage=12, element='Water')

    def apply_effect(self, player, enemy):

        if enemy.element == 'Water':

            return

        bonus_damage = 10 if enemy.element == 'Fire' else 0
        total_damage = self.damage + bonus_damage

        self.damage_sound.play()
        enemy.health -= total_damage

        damage_sprite = DamageNumber(total_damage, enemy.rect.center)
        enemy.all_sprites.add(damage_sprite)

        if enemy.element == 'Fire':

            enemy.burning = True

        knockback_force = pygame.Vector2(enemy.rect.center) - pygame.Vector2(player.rect.center)

        if knockback_force.length() != 0:

            knockback_direction = knockback_force.normalize()
            enemy.apply_knockback(knockback_direction, self.knockback_speed, self.knockback_duration)

# Earth Sword (Greater Knockback Effect)
class EarthSword(Sword):

    def __init__(self):
        super().__init__('Earth Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'earth', 'sword.png')), damage=18, element='Earth')

        self.knockback_speed = EARTHSWORD_KNOCKBACK_SPEED
        self.knockback_duration = EARTHSWORD_KNOCKBACK_DURATION

    def apply_effect(self, player, enemy):

        if enemy.element == 'Earth':

            return

        bonus_damage = 10 if enemy.element != 'Earth' else 0
        total_damage = self.damage + bonus_damage

        self.damage_sound.play()
        enemy.health -= total_damage

        damage_sprite = DamageNumber(total_damage, enemy.rect.center)
        enemy.all_sprites.add(damage_sprite)

        knockback_force = pygame.Vector2(enemy.rect.center) - pygame.Vector2(player.rect.center)

        if knockback_force.length() != 0:

            knockback_direction = knockback_force.normalize()
            enemy.apply_knockback(knockback_direction, self.knockback_speed, self.knockback_duration)

# Air Sword (Chance to Stun)
class AirSword(Sword):

    def __init__(self):

        super().__init__('Air Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'air', 'sword.png')), damage=14, element='Air')

    def apply_effect(self, player, enemy):

        if enemy.element == 'Air':

            return

        bonus_damage = 10 if enemy.element == 'Water' else 0
        total_damage = self.damage + bonus_damage

        self.damage_sound.play()
        enemy.health -= total_damage

        damage_sprite = DamageNumber(total_damage, enemy.rect.center)
        enemy.all_sprites.add(damage_sprite)

        if random.random() < 0.2:

            enemy.stunned = True
            enemy.stun_duration = 2

        knockback_force = pygame.Vector2(enemy.rect.center) - pygame.Vector2(player.rect.center)

        if knockback_force.length() != 0:

            knockback_direction = knockback_force.normalize()
            enemy.apply_knockback(knockback_direction, self.knockback_speed, self.knockback_duration)