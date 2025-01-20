import sys

import pygame.display
from pytmx.util_pygame import load_pygame
from player import Player
from settings import *
from sprites import Sprite

class Game:

    def __init__(self):

        pygame.init()

        # Game window
        self.scene = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Hra')

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Map
        self.load_map()

        # Engine
        self.clock = pygame.time.Clock()
        self.running = True

        player = Player((pygame.display.Info().current_w/2, pygame.display.Info().current_h/2), self.all_sprites, self.collision_sprites)

    def load_map(self):

        tile_map = load_pygame(join('assets', 'map', 'tmx', 'map.tmx'))

        for x, y, image in tile_map.get_layer_by_name('terrain').tiles():
            if image:
                Sprite((x*TILE_SIZE, y*TILE_SIZE), self.all_sprites, image)

        #for item in tile_map.get_layer_by_name('objects non'):
            #if item.image:
                #Sprite((item.x, item.y), self.all_sprites, item.image)

        #for item in tile_map.get_layer_by_name('objects'):
            #if item.image:
                #Sprite((item.x, item.y), (self.all_sprites, self.collision_sprites), item.image)


    def toggle_fullscreen(self):

        if self.fullscreen:
            self.scene = pygame.display.set_mode((WINDOW_W, WINDOW_H))
            self.fullscreen = False

        else:
            self.scene = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

    def run(self):

        while self.running:

            delta = self.clock.tick() / 1000.0

            # Event loop
            for event in pygame.event.get():

                # Quit Event
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

                # Toggle Fullscreen Event
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.toggle_fullscreen()

            # Update
            self.all_sprites.draw(self.scene)
            self.all_sprites.update(delta)
            pygame.display.update()

        pygame.quit()
        sys.exit()