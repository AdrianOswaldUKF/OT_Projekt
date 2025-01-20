from const import *

import sys
import pygame.display
from groups import AllSprites
from tile_map import TileMap

class Game:

    def __init__(self):

        pygame.init()

        # Game window
        self.scene = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Hra')

        # Sprite Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # Map
        self.tile_map = TileMap(join('assets', 'map', 'tmx', 'map.tmx'), self.all_sprites, self.collision_sprites)
        self.tile_map.load_map()

        # Engine
        self.clock = pygame.time.Clock()
        self.running = True


    def toggle_fullscreen(self):

        if self.fullscreen:
            self.scene = pygame.display.set_mode((WINDOW_W, WINDOW_H))
            self.fullscreen = False

        else:
            self.scene = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

    def run(self):

        while self.running:

            delta_time = self.clock.tick() / 1000.0

            # Event loop
            for event in pygame.event.get():

                # Quit Event
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

                # Toggle Fullscreen Event
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.toggle_fullscreen()

            # Update
            self.all_sprites.draw(self.tile_map.player.rect.center)
            self.all_sprites.update(delta_time)
            pygame.display.update()

        pygame.quit()
        sys.exit()