import pygame
import sys
from os.path import join
from const import *
from groups import AllSprites
from tile_map import TileMap, SlimeSpawner
from gui import GUI, InventoryGUI

class Game:

    def __init__(self):

        pygame.init()

        # Game window
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Hra')

        # Sprite Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.interactables_sprites = pygame.sprite.Group()

        # Map
        self.tile_map = TileMap(
            self.display_surface,
            join('assets', 'map', 'tmx', 'test.tmx'),
            self.all_sprites,
            self.collision_sprites,
            self.enemy_sprites,
            self.interactables_sprites
        )
        self.tile_map.load_tilemap()

        # Player
        self.player = self.tile_map.player

        # User Interface
        self.gui = GUI(self.display_surface, self.player)

        # Enemies
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)

        # Engine
        self.clock = pygame.time.Clock()
        self.running = True

        # FPS
        self.fps_update_interval = 1000  # Update FPS every 1000 milliseconds (1 second)
        self.last_fps_update_time = pygame.time.get_ticks()
        self.frame_count = 0
        self.current_fps = 0

        # Inventory GUI
        self.inventory_gui = InventoryGUI(self.display_surface, self.player)

    def toggle_fullscreen(self):

        if self.fullscreen:
            self.display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H)) # const.py
            self.fullscreen = False

        else:
            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

    def update_fps(self):
        # Get current time in milliseconds
        current_time = pygame.time.get_ticks()
        self.frame_count += 1

        # Update FPS every second (1000 ms)
        if current_time - self.last_fps_update_time >= self.fps_update_interval:
            self.current_fps = round(self.frame_count / (self.fps_update_interval / 1000))  # Calculate FPS
            self.last_fps_update_time = current_time
            self.frame_count = 0  # Reset frame count for the next second

    def check_collisions(self, delta_time):

        if not self.player.alive:
            return

        for enemy in self.enemy_sprites:
            if self.player.rect.colliderect(enemy.hitbox_rect):
                enemy.deal_damage(delta_time)

    def update_spawners(self):
        for spawner in self.tile_map.spawners:
            spawner.spawn()

    def run(self):
        while self.running:
            delta_time = self.clock.tick() / 1000.0

            # Event loop
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

                # Toggle fullscreen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.toggle_fullscreen()

                # Interact
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.player.interact()

                # Toggle inventory
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    self.inventory_gui.toggle_inventory()

            # In your main game loop
            if self.inventory_gui.inventory_visible:
                # Handle keyboard input for equipping items
                self.inventory_gui.handle_input(self.player)

                # Handle mouse input for switching items
                if pygame.mouse.get_pressed()[0]:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    self.inventory_gui.handle_mouse_input(mouse_pos, self.player, self.player.inventory)

            self.update_spawners()

            # Update
            self.display_surface.fill((0, 255, 255))  # Example background color
            self.all_sprites.draw(self.player.rect.center)
            self.all_sprites.update(delta_time)
            self.check_collisions(delta_time)

            # Update FPS
            self.update_fps()

            # Draw GUI
            self.gui.draw_health_bar(self.player.health, 100)
            self.gui.draw_health_text(self.player.health)
            self.gui.draw_fps(self.current_fps)

            # Draw Inventory if visible
            self.inventory_gui.draw_inventory(self.player.inventory)

            pygame.display.update()

        pygame.quit()
        sys.exit()
