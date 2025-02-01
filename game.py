import pygame
import sys
from os.path import join
from const import *
from groups import AllSprites
from object import ITEM_PICKUP_EVENT
from tile_map import TileMap, SlimeSpawner
from gui import GUI, InventoryGUI

class Game:

    def __init__(self):

        pygame.init()

        # Game window
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Slimes Invade')

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

        self.font = pygame.font.Font(None, 100)
        self.restart_button = pygame.Rect(pygame.display.Info().current_w // 2 - 100, pygame.display.Info().current_h // 2 + 50, 200, 50)

        self.player_won = False
        self.quit_button = pygame.Rect(
            pygame.display.Info().current_w // 2 - 100,
            pygame.display.Info().current_h // 2 + 50,
            200, 50
        )


    def toggle_fullscreen(self):

        if self.fullscreen:

            self.display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H)) # const.py
            self.fullscreen = False

        else:

            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

        self.restart_button = pygame.Rect(pygame.display.Info().current_w // 2 - 100,
                                          pygame.display.Info().current_h // 2 + 50, 200, 50)

    def update_fps(self):

        current_time = pygame.time.get_ticks()
        self.frame_count += 1

        if current_time - self.last_fps_update_time >= self.fps_update_interval:

            self.current_fps = round(self.frame_count / (self.fps_update_interval / 1000))
            self.last_fps_update_time = current_time
            self.frame_count = 0

    def check_collisions(self, delta_time):

        if not self.player.alive:

            return

        for enemy in self.enemy_sprites:

            if self.player.rect.colliderect(enemy.hitbox_rect):

                enemy.deal_damage(delta_time)

    def update_spawners(self):

        for spawner in self.tile_map.spawners:

            spawner.update()

        if not self.tile_map.spawners:

            self.player_won = True

    def draw_game_over_screen(self):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        dark_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        dark_surface.fill((30, 30, 30, 150))

        self.display_surface.blit(dark_surface, (0, 0))

        game_over_text = self.font.render("You are dead", True, (255, 0, 0))
        self.display_surface.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))

        restart_text = self.font.render("Restart", True, (255, 255, 255))

        restart_button_width = restart_text.get_width() + 20
        restart_button_height = restart_text.get_height() + 10
        self.restart_button = pygame.Rect(screen_width // 2 - restart_button_width // 2, screen_height // 2 + 50, restart_button_width, restart_button_height)

        pygame.draw.rect(self.display_surface, (100, 100, 100), self.restart_button, border_radius=10)
        pygame.draw.rect(self.display_surface, (0, 0, 0, 0), self.restart_button, width=2)
        self.display_surface.blit(restart_text, (self.restart_button.centerx - restart_text.get_width() // 2,
                                                      self.restart_button.centery - restart_text.get_height() // 2))

    def draw_win_screen(self):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        dark_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        dark_surface.fill((30, 30, 30, 150))
        self.display_surface.blit(dark_surface, (0, 0))

        win_text = self.font.render("You Win!", True, (0, 255, 0))
        self.display_surface.blit(
            win_text,
            (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 100)
        )

        quit_text = self.font.render("Quit", True, (255, 255, 255))

        padding = 20
        quit_button_width = quit_text.get_width() + padding
        quit_button_height = quit_text.get_height() + padding
        self.quit_button = pygame.Rect(
            screen_width // 2 - quit_button_width // 2,
            screen_height // 2 + 50,
            quit_button_width,
            quit_button_height
        )

        pygame.draw.rect(self.display_surface, (100, 100, 100), self.quit_button, border_radius=10)
        pygame.draw.rect(self.display_surface, (0, 0, 0), self.quit_button, width=2)

        self.display_surface.blit(
            quit_text,
            (self.quit_button.centerx - quit_text.get_width() // 2,
             self.quit_button.centery - quit_text.get_height() // 2)
        )

    def handle_restart(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.restart_button.collidepoint(mouse_pos):

            if pygame.mouse.get_pressed()[0]:

                self.reset_game()

    def reset_game(self):

        # Reset the game state
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()
        self.interactables_sprites.empty()

        # Reload map and player
        self.tile_map.load_tilemap()
        self.player = self.tile_map.player

        # Reset player health
        self.player.health = 100
        self.player.alive = True

        # Restart GUI
        self.gui = GUI(self.display_surface, self.player)

    def run(self):

        while self.running:

            delta_time = self.clock.tick() / 1000.0

            mouse_pos = pygame.mouse.get_pos()

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


                # Handle item pickup messages
                if event.type == ITEM_PICKUP_EVENT:

                    self.gui.show_pickup_message(event.message)

            self.player.handle_item_switch()

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
            self.gui.draw_pickup_message()
            self.inventory_gui.draw_toolbar()
            self.inventory_gui.handle_mouse_input(mouse_pos, self.player)

            # Check if player is dead
            if not self.player.alive:
                self.draw_game_over_screen()
                self.handle_restart()

            if self.player_won:
                self.draw_win_screen()

                mouse_pos = pygame.mouse.get_pos()
                if self.quit_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    self.running = False

            pygame.display.update()

        pygame.quit()
        sys.exit()
