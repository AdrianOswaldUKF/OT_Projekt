import pygame

class AllSprites(pygame.sprite.Group):

    def __init__(self):

        super().__init__()

        self.scene = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):

        self.offset.x = -(target_pos[0] - pygame.display.Info().current_w / 2)
        self.offset.y = -(target_pos[1] - pygame.display.Info().current_h / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'terrain')]
        player_sprite = [sprite for sprite in self if hasattr(sprite, 'isPlayer')]
        enemy_sprites = [sprite for sprite in self if hasattr(sprite, 'isEnemy')]
        object_sprites = [sprite for sprite in self if hasattr(sprite, 'object')]

        for layer in [ground_sprites, player_sprite, enemy_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)
