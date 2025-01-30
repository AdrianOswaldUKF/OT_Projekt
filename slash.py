import pygame
from os.path import join

from const import SLASH_SPEED


class Slash(pygame.sprite.Sprite):

    def __init__(self, attack_rect, position, direction, sword_type, groups):

        super().__init__(groups)

        self.isSlash = True


        # Position and direction of the slash
        self.attack_rect = attack_rect
        self.position = position
        self.direction = direction
        self.frame = 0

        # Slash animation images
        self.slash_animation_sprites = []
        self.load_slash_images(sword_type)

        # Image and rect
        self.image = self.slash_animation_sprites[0]
        self.rect = self.image.get_rect(center=position)

    def load_slash_images(self, sword_type):

        self.slash_animation_sprites = []

        sword_type = sword_type.lower().split()[0]

        for i in range(6):

            file_path = join('assets', 'sprites', 'weapons', sword_type, f'slash{i + 1}.png')

            if file_path:
                self.slash_animation_sprites.append(pygame.image.load(file_path).convert_alpha())
                self.slash_animation_sprites[i] = pygame.transform.scale(self.slash_animation_sprites[i], self.attack_rect.size)

    def update(self, delta_time):

        self.frame += SLASH_SPEED * delta_time

        if int(self.frame) >= len(self.slash_animation_sprites):
            self.kill()
        else:
            self.image = self.slash_animation_sprites[int(self.frame)]
