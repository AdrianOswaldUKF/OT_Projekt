import pygame
import sys
from os.path import join
from const import *
from groups import AllSprites
from object import ITEM_PICKUP_EVENT
from tile_map import TileMap
from gui import GUI, InventoryGUI

class Game:

    def __init__(self, display_surface, fullscreen):

        pygame.init()

        # Game window
        self.display_surface = display_surface
        self.fullscreen = fullscreen
        pygame.display.set_caption('Slimes Invade')

        # Sprite Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.interactables_sprites = pygame.sprite.Group()

        # Map
        self.tile_map = TileMap(
            self.display_surface,
            join('assets', 'map', 'tmx', 'level_1.tmx'),
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

        # Font
        self.font = pygame.font.Font(None, 100)

        # Restart button
        self.restart_button = pygame.Rect(pygame.display.Info().current_w // 2 - 100, pygame.display.Info().current_h // 2 + 50, 200, 50)

        self.player_won = False

        # Quit button
        self.quit_button = pygame.Rect(
            pygame.display.Info().current_w // 2 - 100,
            pygame.display.Info().current_h // 2 + 50,
            200, 50
        )

        # Music
        self.game_music = pygame.mixer.Sound(join('assets', 'sounds', 'game', 'game.wav'))
        self.game_music.set_volume(0.1)
        self.game_music.play(loops=-1)

        self.paused = False


    def toggle_fullscreen(self):

        if self.fullscreen:

            self.display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H)) # const.py
            self.fullscreen = False

        else:

            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

        self.restart_button = pygame.Rect(pygame.display.Info().current_w // 2 - 100,
                                          pygame.display.Info().current_h // 2 + 50, 200, 50)

    def toggle_pause(self):

        self.paused = not self.paused

    def draw_pause_menu(self):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        # Pause text
        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        self.display_surface.blit(pause_text,
                                  (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - 100))

        # Button styling
        continue_text = self.font.render("Continue", True, (255, 255, 255))
        quit_text = self.font.render("Quit", True, (255, 255, 255))

        continue_button_width = continue_text.get_width() + 20
        continue_button_height = continue_text.get_height() + 10
        continue_button = pygame.Rect(screen_width // 2 - continue_button_width // 2,
                                      screen_height // 2 + 50, continue_button_width, continue_button_height)

        quit_button_width = quit_text.get_width() + 20
        quit_button_height = quit_text.get_height() + 10
        quit_button = pygame.Rect(screen_width // 2 - quit_button_width // 2,
                                  screen_height // 2 + 150, quit_button_width, quit_button_height)

        # Draw buttons
        pygame.draw.rect(self.display_surface, (60, 60, 60), continue_button, border_radius=12)
        pygame.draw.rect(self.display_surface, (50, 50, 50), continue_button, border_radius=12, width=3)
        pygame.draw.rect(self.display_surface, (60, 60, 60), quit_button, border_radius=12)
        pygame.draw.rect(self.display_surface, (50, 50, 50), quit_button, border_radius=12, width=3)

        return continue_button, quit_button, continue_text, quit_text

    def handle_pause_menu(self):

        mouse_pos = pygame.mouse.get_pos()
        continue_button, quit_button, continue_text, quit_text = self.draw_pause_menu()

        # Hover effect
        if continue_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.display_surface, (80, 80, 80), continue_button, border_radius=12)
            pygame.draw.rect(self.display_surface, (50, 50, 50), continue_button, border_radius=12, width=3)

        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.display_surface, (80, 80, 80), quit_button, border_radius=12)
            pygame.draw.rect(self.display_surface, (50, 50, 50), quit_button, border_radius=12, width=3)


        self.display_surface.blit(continue_text, (continue_button.centerx - continue_text.get_width() // 2,
                                                  continue_button.centery - continue_text.get_height() // 2))
        self.display_surface.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                              quit_button.centery - quit_text.get_height() // 2))

        if continue_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:

            self.toggle_pause()

        if quit_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:

            self.running = False

    def update_fps(self):

        current_time = pygame.time.get_ticks()
        self.frame_count += 1

        if current_time - self.last_fps_update_time >= self.fps_update_interval:

            self.current_fps = round(self.frame_count / (self.fps_update_interval / 1000))
            self.last_fps_update_time = current_time
            self.frame_count = 0

    def check_collisions(self, delta_time):

        # If player is not alive do not check collisions
        if not self.player.alive:

            return

        # If colliding with player, deal damage
        for enemy in self.enemy_sprites:

            if self.player.rect.colliderect(enemy.hitbox_rect):

                enemy.deal_damage(delta_time)

    def update_spawners(self):

        # Update spawners on map
        for spawner in self.tile_map.spawners:

            spawner.update()

        # If not any spawners left on the map then the player has won
        if not self.tile_map.spawners:

            self.player_won = True

    def draw_game_over_screen(self):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        # Dark background with transparency
        dark_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        dark_surface.fill((30, 30, 30, 150))

        self.display_surface.blit(dark_surface, (0, 0))

        # Text
        game_over_text = self.font.render("You are dead", True, (255, 0, 0))
        self.display_surface.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))

        restart_text = self.font.render("Restart", True, (255, 255, 255))

        # Button position
        restart_button_width = restart_text.get_width() + 20
        restart_button_height = restart_text.get_height() + 10
        self.restart_button = pygame.Rect(screen_width // 2 - restart_button_width // 2, screen_height // 2 + 50, restart_button_width, restart_button_height)

        pygame.draw.rect(self.display_surface, (100, 100, 100), self.restart_button, border_radius=10)
        pygame.draw.rect(self.display_surface, (0, 0, 0, 0), self.restart_button, width=2)
        self.display_surface.blit(restart_text, (self.restart_button.centerx - restart_text.get_width() // 2,
                                                      self.restart_button.centery - restart_text.get_height() // 2))

    def draw_win_screen(self):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        # Dark background with transparency
        dark_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        dark_surface.fill((30, 30, 30, 150))
        self.display_surface.blit(dark_surface, (0, 0))

        # Text
        win_text = self.font.render("You Win!", True, (0, 255, 0))
        self.display_surface.blit(
            win_text,
            (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 100)
        )

        quit_text = self.font.render("Quit", True, (255, 255, 255))

        # Button styling
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

        # Reset all sprite groups
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()
        self.interactables_sprites.empty()
        self.tile_map.spawners.clear()

        # Reload map and player
        self.tile_map.load_tilemap()
        self.player = self.tile_map.player
        self.player.health = 100
        self.player.alive = True

        # Restart GUI
        self.gui = GUI(self.display_surface, self.player)
        self.inventory_gui = InventoryGUI(self.display_surface, self.player)

        # Reset progression flags
        self.player_won = False

    def run(self):

        while self.running:

            delta_time = self.clock.tick() / 1000.0

            mouse_pos = pygame.mouse.get_pos()

            # Event loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        self.toggle_pause()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:

                        self.toggle_fullscreen()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:

                        self.player.interact()

                if self.paused:

                    self.handle_pause_menu()
                    pygame.display.update()

                    continue

                if event.type == ITEM_PICKUP_EVENT:

                    self.gui.show_pickup_message(event.message)

            if not self.paused:

                self.player.handle_item_switch()
                self.update_spawners()

                # Update
                self.display_surface.fill((61, 139, 175))
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

                # Check if player is dead or has won
                if not self.player.alive:

                    self.draw_game_over_screen()
                    self.handle_restart()

                # If player won then draw the win screen
                if self.player_won:

                    self.draw_win_screen()

                    mouse_pos = pygame.mouse.get_pos()

                    if self.quit_button.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed()[0]:
                            self.running = False

            pygame.display.update()

        pygame.quit()
        sys.exit()