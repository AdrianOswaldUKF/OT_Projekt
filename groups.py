import pygame

class AllSprites(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        self.scene = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        # Calculate offset to center the camera on the player
        self.offset.x = -(target_pos[0] - pygame.display.Info().current_w / 2)
        self.offset.y = -(target_pos[1] - pygame.display.Info().current_h / 2)

        # Separate sprites into categories
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'terrain')]
        player_sprite = [sprite for sprite in self if hasattr(sprite, 'isPlayer')]
        enemy_sprites = [sprite for sprite in self if hasattr(sprite, 'isEnemy')]
        object_sprites = [sprite for sprite in self if hasattr(sprite, 'object')]
        slash_sprites = [sprite for sprite in self if hasattr(sprite, 'isSlash')]

        # First, render the ground and enemy sprites, which always render behind the player and objects
        for layer in [ground_sprites, enemy_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Combine all sprites (player + objects) and sort them
        all_sprites = player_sprite + object_sprites
        if player_sprite:
            sorted_sprites = sorted(all_sprites, key=lambda sprite: (sprite.rect.centery, isinstance(sprite, type(player_sprite[0]))))
        else:
            sorted_sprites = sorted(all_sprites, key=lambda sprite: sprite.rect.centery)

        # Render the sorted sprites (player + objects)
        for sprite in sorted_sprites:
            self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Render slashes separately
        for slash in slash_sprites:
            self.scene.blit(slash.image, slash.rect.topleft + self.offset)