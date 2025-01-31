import pygame
from abc import abstractmethod

class Entity(pygame.sprite.Sprite):

    def __init__(self, groups):

        super().__init__(groups)

        # Sprites, Hitbox
        self.collision_sprites = None
        self.hitbox_rect = None
        self.direction = None

        # Health
        self.health = 0
        self.alive = True

    def collision(self, direction):

        for sprite in self.collision_sprites:

            if sprite.rect.colliderect(self.hitbox_rect):

                if direction == 'horizontal':

                    if self.direction.x > 0:  # Moving right

                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:  # Moving left

                        self.hitbox_rect.left = sprite.rect.right

                if direction == 'vertical':

                    if self.direction.y > 0:  # Moving down

                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # Moving up

                        self.hitbox_rect.top = sprite.rect.bottom

                return True  # Return immediately if a collision is detected

        return False  # If no collision is detected, return False

    @abstractmethod
    def move(self, delta_time):

        pass

    @abstractmethod
    def animate(self, delta_time):

        pass

    @abstractmethod
    def update(self, delta_time):

        pass