import pygame
import os
from item import Item  # Import Item from item.py

class Sword(Item):
    def __init__(self, name, image, damage, element, attack_range=50, equippable=True):
        super().__init__(name, image, equippable)
        self.damage = damage
        self.attack_range = attack_range  # Range of the sword attack
        self.element = element  # Element type

    def attack(self, player, enemies):
        if self.equipped:
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect.inflate(self.attack_range, self.attack_range)):
                    enemy.health -= self.damage
                    print(f"{enemy.enemy_name} took {self.damage} {self.element} damage!")
                    if enemy.health <= 0:
                        print(f"{enemy.enemy_name} has been defeated!")


# Specific Elemental Swords
class BasicSword(Sword):
    def __init__(self):
        super().__init__("Basic Sword", pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'basic', 'sword.png')), damage=10, element="None")

class FireSword(Sword):
    def __init__(self):
        super().__init__("Fire Sword", pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'fire', 'sword.png')), damage=15, element="Fire")

class WaterSword(Sword):
    def __init__(self):
        super().__init__("Water Sword", pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'water', 'sword.png')), damage=12, element="Water")

class EarthSword(Sword):
    def __init__(self):
        super().__init__("Earth Sword", pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'earth', 'sword.png')), damage=18, element="Earth")

class AirSword(Sword):
    def __init__(self):
        super().__init__("Air Sword", pygame.image.load(os.path.join('assets', 'sprites', 'weapons', 'air', 'sword.png')), damage=14, element="Air")
