import os.path

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

class HealingPotion(pygame.sprite.Sprite):

    def __init__(self, x, y, player, groups):

        super().__init__(groups)

        self.image = pygame.image.load(os.path.join('assets', 'sprites', 'items', 'healing_potion', '0.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 20))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.player = player
        self.heal_amount = 20
        self.isHealingPotion = True


    def update(self, delta_time):

        if self.rect.colliderect(self.player.rect):

            self.player.heal(self.heal_amount)
            self.kill()