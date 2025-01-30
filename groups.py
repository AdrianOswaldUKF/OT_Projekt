import pygame

class AllSprites(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        self.scene = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):

        # Offset
        self.offset.x = -(target_pos[0] - pygame.display.Info().current_w / 2)
        self.offset.y = -(target_pos[1] - pygame.display.Info().current_h / 2)

        # Categories
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'terrain')]
        player_sprite = [sprite for sprite in self if hasattr(sprite, 'isPlayer')]
        enemy_sprites = [sprite for sprite in self if hasattr(sprite, 'isEnemy')]
        object_sprites = [sprite for sprite in self if hasattr(sprite, 'object')]
        slash_sprites = [sprite for sprite in self if hasattr(sprite, 'isSlash')]

        # Ground
        for layer in [ground_sprites, enemy_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Combine Player + Objects and sort
        all_sprites = player_sprite + object_sprites
        if player_sprite:
            sorted_sprites = sorted(all_sprites, key=lambda sprite: (sprite.rect.centery, isinstance(sprite, type(player_sprite[0]))))
        else:
            sorted_sprites = sorted(all_sprites, key=lambda sprite: sprite.rect.centery)

        # Player + Objects
        for sprite in sorted_sprites:
            self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Slashes
        for slash in slash_sprites:
            self.scene.blit(slash.image, slash.rect.topleft + self.offset)

        for sprite in enemy_sprites:
            if hasattr(sprite, 'render_health_bar'):
                sprite.render_health_bar(self.scene, self.offset)