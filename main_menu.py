import pygame
import sys
from const import *
from game import Game


class MainMenu:

    def __init__(self, display_surface):

        # Game window
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption('Hra')

        # Fonts
        self.font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 50)

        # Button setup
        self.start_button = pygame.Rect(pygame.display.Info().current_w // 2 - 150,
                                        pygame.display.Info().current_h // 2 + 50, 300, 50)
        self.running = True

        # Button colors
        self.button_color = (0, 200, 0)
        self.button_hover_color = (0, 255, 0)

    def draw_main_menu(self):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        # Gradient background
        self.draw_gradient_background(screen_width, screen_height)

        # Title text with a shadow effect
        self.draw_title(screen_width, screen_height)

        # Draw the Start button with hover effect
        self.draw_start_button()

    def draw_gradient_background(self, width, height):

        for y in range(height):

            color = (0, 0, int(255 * y / height))
            pygame.draw.line(self.display_surface, color, (0, y), (width, y))

    def draw_title(self, width, height):

        title_text = self.font.render("Slimes Invade", True, (255, 255, 255))
        shadow_text = self.font.render("Slimes Invade", True, (50, 50, 50))

        # Shadow slightly offset
        self.display_surface.blit(shadow_text, (width // 2 - shadow_text.get_width() // 2 + 5, height // 2 - 150 + 5))
        self.display_surface.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 150))

    def draw_start_button(self):

        # Hover effect
        mouse_pos = pygame.mouse.get_pos()

        if self.start_button.collidepoint(mouse_pos):

            pygame.draw.rect(self.display_surface, self.button_hover_color, self.start_button, border_radius=15)
        else:

            pygame.draw.rect(self.display_surface, self.button_color, self.start_button, border_radius=15)

        # Button text
        start_text = self.button_font.render("Start", True, (255, 255, 255))
        self.display_surface.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2,
                                               self.start_button.centery - start_text.get_height() // 2))

    def handle_menu_input(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.start_button.collidepoint(mouse_pos):

            if pygame.mouse.get_pressed()[0]:

                return False

        return True

    def toggle_fullscreen(self):

        if self.fullscreen:

            self.display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))  # const.py
            self.fullscreen = False
        else:

            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True

        self.start_button = pygame.Rect(pygame.display.Info().current_w // 2 - 150,
                                        pygame.display.Info().current_h // 2 + 50, 300, 50)

    def run(self):

        while self.running:

            self.display_surface.fill((0, 0, 0))  # Clear the screen

            self.draw_main_menu()  # Draw the menu

            # Event loop
            for event in pygame.event.get():

                # Quit event
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):

                    pygame.quit()
                    sys.exit()

                # Toggle fullscreen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:

                    self.toggle_fullscreen()

            # Handle button click
            self.running = self.handle_menu_input()

            pygame.display.update()

        return Game()  # Launch Game
