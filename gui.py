import pygame

class GUI:

    def __init__(self, screen):

        self.display_surface = screen
        self.display_w = self.display_surface.get_width()
        self.display_h = self.display_surface.get_height()
        self.gui_surface = pygame.Surface(screen.get_size())
        self.font = pygame.font.Font(None, 36)

    def draw_health_bar(self, current_health, max_health):

        # Dimensions
        bar_width = 300
        bar_height = 20
        bar_x = 20
        bar_y = 20

        # Health bar
        health_bar = current_health / max_health

        # Background
        pygame.draw.rect(self.display_surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Current Health
        pygame.draw.rect(self.display_surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_bar, bar_height))

    def draw_health_text(self, current_health):

        health_text = f'Health: {current_health}'
        text_surface = self.font.render(health_text, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (20, 50))

    def draw_fps(self, current_fps):

        fps_text = f'FPS: {current_fps}'
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.display_surface.blit(fps_surface, (self.display_w - 150, 10))