import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, name, equippable=False):

        super().__init__()
        self.name = name
        self.equippable = equippable
        self.equipped = False

    def equip(self, player):

        if self.equippable:
            player.equipped = self  # Equip the item
            self.equipped = True

    def unequip(self, player):

        if self.equippable:
            player.equipped = None
            self.equipped = False


class Sword(Item):

    def __init__(self, name, damage, equippable=True):
        super().__init__(name, equippable)
        self.damage = damage
        self.attack_range = 50  # Range of the sword attack

    def attack(self, player, enemies):
        if self.equipped:
            # Check for enemies within attack range and deal damage
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect.inflate(self.attack_range, self.attack_range)):
                    enemy.health -= self.damage
                    print(f"{enemy.enemy_name} took {self.damage} damage!")
                    if enemy.health <= 0:
                        print(f"{enemy.enemy_name} has been defeated!")
