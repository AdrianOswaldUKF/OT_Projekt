from settings import *

class Sprite(pygame.sprite.Sprite):

    def __init__(self, position, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)