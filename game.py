import pygame
import sys
from os.path import join
from const import *
from groups import AllSprites
from tile_map import TileMap
from gui import GUI

class Game:

    def __init__(self):

        pygame.init()

        # Game window
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Hra')

        # User Interface
        self.gui = GUI(self.display_surface)

        # Sprite Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Map
        self.tile_map = TileMap(join('assets', 'map', 'tmx', 'test.tmx'), self.all_sprites, self.collision_sprites, self.enemy_sprites)
        self.tile_map.load_tilemap()

        # Player

        self.player = self.tile_map.player

        # Enemies
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)

        # Engine
        self.clock = pygame.time.Clock()
        self.running = True

    def toggle_fullscreen(self):

        if self.fullscreen:
            self.display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H)) # const.py
            self.fullscreen = False

        else:
            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True


    def check_collisions(self, delta_time):

        if not self.player.alive:
            return

        for enemy in self.enemy_sprites:
            if self.player.hitbox_rect.colliderect(enemy.hitbox_rect):
                enemy.deal_damage(delta_time)

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

                # if event.type == self.enemy_event:
                #     position = choice(self.tile_map.enemy_spawn_positions)
                #     enemy = choice(list(self.tile_map.enemy_frames.values()))
                #     Enemy(position, enemy, (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # Update
            self.display_surface.fill((0, 255, 255))
            self.all_sprites.draw(self.player.rect.center)
            self.all_sprites.update(delta_time)
            self.check_collisions(delta_time)

            # Draw GUI
            self.gui.draw_health_bar(self.player.health, 100)
            self.gui.draw_health_text(self.player.health)

            pygame.display.update()

        pygame.quit()
        sys.exit()