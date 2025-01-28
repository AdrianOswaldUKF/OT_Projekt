import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, name, equippable=False):

        super().__init__()
        self.name = name
        self.equippable = equippable
        self.equipped = False

    def use(self, player):

        if self.equippable:
            player.equipped = self  # Equip the item
            self.equipped = True

    def unequip(self, player):

        if self.equippable:
            player.equipped = None
            self.equipped = False

class Sword(Item):

    def __init__(self, name, equippable=True):
        super().__init__(name, equippable)