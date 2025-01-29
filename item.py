import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, image, equippable=False):
        super().__init__()
        self.name = name
        self.equippable = equippable
        self.equipped = False

        # Sprite
        self.image = image
        self.rect = self.image.get_frect()

    def equip(self, player):
        if self.equippable:
            player.equipped = self  # Equip the item
            self.equipped = True

    def unequip(self, player):
        if self.equippable:
            player.equipped = None
            self.equipped = False