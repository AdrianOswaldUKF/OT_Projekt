import pygame
import random
import os
from item import Item

class Sword(Item):
    def __init__(self, name, image, damage, element, attack_range=50, equippable=True):
        super().__init__(name, image, equippable)
        self.damage = damage
        self.attack_range = attack_range
        self.element = element

    def attack(self, attack_rect, player, enemies):

        if self.equipped:
            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):  # Check if enemy is within range
                    self.apply_effect(player, enemy)

    def apply_effect(self, player, enemy):

        enemy.health -= self.damage

# Basic Sword (No Special Effect)
class BasicSword(Sword):
    def __init__(self):
        super().__init__('Basic Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'basic', 'sword.png')), damage=10, element='None')

# Fire Sword (Burns Non-Fire Slimes)
class FireSword(Sword):
    def __init__(self):
        super().__init__('Fire Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'fire', 'sword.png')), damage=15, element='Fire')

    def apply_effect(self, player, enemy):
        enemy.health -= self.damage

        if enemy.element != 'Fire' and enemy.element !='Water':  # Assuming enemy has an `element` attribute
            enemy.burning = True  # Set enemy on fire

# Water Sword (Extra Damage to Fire Slimes)
class WaterSword(Sword):
    def __init__(self):
        super().__init__('Water Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'water', 'sword.png')), damage=12, element='Water')

    def apply_effect(self, player, enemy):
        bonus_damage = 8 if enemy.element == 'Fire' else 0
        total_damage = self.damage + bonus_damage
        enemy.health -= total_damage

# Earth Sword (Knockback Effect)
class EarthSword(Sword):
    def __init__(self):
        super().__init__('Earth Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'earth', 'sword.png')), damage=18, element='Earth')

    def apply_effect(self, player, enemy):
        enemy.health -= self.damage
        knockback_force = pygame.Vector2(enemy.rect.center) - pygame.Vector2(player.rect.center)
        if knockback_force.length() != 0:
            enemy.direction = knockback_force.normalize() * 3  # Push enemy back

# Air Sword (Chance to Stun)
class AirSword(Sword):
    def __init__(self):
        super().__init__('Air Sword', pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'air', 'sword.png')), damage=14, element='Air')

    def apply_effect(self, player, enemy):
        enemy.health -= self.damage
        if random.random() < 0.2:  # 20% chance to stun
            enemy.stunned = True  # Set enemy stunned
            enemy.stun_duration = 2  # Stun lasts 2 seconds
