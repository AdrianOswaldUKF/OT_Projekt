import pygame

class Item(pygame.sprite.Sprite):

    def __init__(self, screen, player):

        super().__init__()

        self.screen = screen
        self.player = player