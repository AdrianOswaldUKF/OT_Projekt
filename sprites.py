import pygame

class Sprite(pygame.sprite.Sprite):

    def __init__(self, position, groups, surface):

        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.terrain = True

class CollisionSprite(pygame.sprite.Sprite):

    def __init__(self, position, groups, surface):

        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.object = True
