import os
import pygame
import sys
from const import *
from game import Game


class MainMenu:

    def __init__(self):
        # Game window
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Hra')

        # Fonts
        self.font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 50)

        # Button positions (dynamic)
        self.update_buttons()

        # Button colors
        self.button_color = (0, 200, 0)
        self.button_hover_color = (0, 255, 0)

        self.running = True

        # Load menu music
        self.menu_music = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'menu', 'menu.wav'))
        self.menu_music.set_volume(0.2)
        self.menu_music.play(loops=-1)

        # Load background image
        self.original_bg = pygame.image.load(os.path.join('assets', 'images', 'menu', 'main_menu.png'))
        self.background_image = self.get_scaled_background()

    def update_buttons(self):

        screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.start_button = pygame.Rect(screen_w // 2 - 150, screen_h // 2, 300, 50)
        self.quit_button = pygame.Rect(screen_w // 2 - 150, self.start_button.bottom + 20, 300, 50)

    def get_scaled_background(self):

        screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h

        return pygame.transform.smoothscale(self.original_bg, (screen_w, screen_h))

    def draw_main_menu(self):

        self.display_surface.blit(self.background_image, (0, 0))
        self.draw_title()
        self.draw_buttons()

    def draw_title(self):

        screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h

        title_text = self.font.render("Slimes Invade", True, (255, 255, 255))
        shadow_text = self.font.render("Slimes Invade", True, (50, 50, 50))

        self.display_surface.blit(shadow_text, (screen_w // 2 - shadow_text.get_width() // 2 + 5,
                                                screen_h // 2 - 150 + 5))
        self.display_surface.blit(title_text, (screen_w // 2 - title_text.get_width() // 2, screen_h // 2 - 150))

    def draw_buttons(self):

        mouse_pos = pygame.mouse.get_pos()

        for button, text in [(self.start_button, "Start"), (self.quit_button, "Quit")]:

            color = self.button_hover_color if button.collidepoint(mouse_pos) else self.button_color
            pygame.draw.rect(self.display_surface, color, button, border_radius=15)

            text_surf = self.button_font.render(text, True, (255, 255, 255))
            self.display_surface.blit(text_surf, (button.centerx - text_surf.get_width() // 2,
                                                  button.centery - text_surf.get_height() // 2))

    def handle_menu_input(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.start_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:

            self.menu_music.stop()
            return False  # Exit menu

        if self.quit_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:

            pygame.quit()
            sys.exit()

        return True  # Keep menu running

    def toggle_fullscreen(self):

        if self.fullscreen:

            self.display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))  # Use windowed size from const.py
            self.fullscreen = False
        else:

            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

        self.update_buttons()
        self.background_image = self.get_scaled_background()  # Rescale background

    def run(self):


        while self.running:

            self.display_surface.fill((0, 0, 0))
            self.draw_main_menu()

            for event in pygame.event.get():

                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):

                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:

                    self.toggle_fullscreen()

            self.running = self.handle_menu_input()

            pygame.display.update()

        return Game(self.display_surface, self.fullscreen)
