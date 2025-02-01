import pygame

class AllSprites(pygame.sprite.Group):

    def __init__(self):

        super().__init__()
        self.scene = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.offset.x = -(target_pos[0] - screen_width / 2)
        self.offset.y = -(target_pos[1] - screen_height / 2)

        camera_rect = pygame.Rect(-self.offset.x, -self.offset.y, screen_width, screen_height)

        visible_sprites = [sprite for sprite in self if camera_rect.colliderect(sprite.rect)]

        # Categorize only visible sprites
        ground_sprites = [sprite for sprite in visible_sprites if hasattr(sprite, 'terrain')]
        player_sprite = [sprite for sprite in visible_sprites if hasattr(sprite, 'isPlayer')]
        enemy_sprites = [sprite for sprite in visible_sprites if hasattr(sprite, 'isEnemy')]
        object_sprites = [sprite for sprite in visible_sprites if hasattr(sprite, 'object')]
        item_sprites = [sprite for sprite in visible_sprites if hasattr(sprite, 'isHealingPotion')]
        slash_sprites = [sprite for sprite in visible_sprites if hasattr(sprite, 'isSlash')]
        damage_number_sprites = [sprite for sprite in visible_sprites if hasattr(sprite, 'isDamageNumber')]

        # Draw ground
        for layer in [ground_sprites, enemy_sprites]:

            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):

                self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Sort Player + Objects
        all_sprites = player_sprite + object_sprites
        sorted_sprites = sorted(all_sprites, key=lambda sprite: (
        sprite.rect.centery, isinstance(sprite, type(player_sprite[0])))) if player_sprite else sorted(all_sprites, key=lambda
            sprite: sprite.rect.centery)

        for sprite in sorted_sprites:

            self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)

        # Render slashes and items
        for slash in slash_sprites:

            self.scene.blit(slash.image, slash.rect.topleft + self.offset)

        for item in item_sprites:

            self.scene.blit(item.image, item.rect.topleft + self.offset)

        for sprite in enemy_sprites:

            if hasattr(sprite, 'render_health_bar'):

                sprite.render_health_bar(self.scene, self.offset)

        for sprite in sorted(damage_number_sprites, key=lambda s: s.rect.centery):

            self.scene.blit(sprite.image, sprite.rect.topleft + self.offset)
