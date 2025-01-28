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


class InventoryGUI(GUI):

    def __init__(self, screen):

        super().__init__(screen)

        # Inventory UI settings
        self.inventory_bg_color = (50, 50, 50)  # Background color
        self.inventory_border_color = (200, 200, 200)  # Border color
        self.text_color = (255, 255, 255)  # Item text color
        self.inventory_visible = False  # Whether inventory is displayed

    def toggle_inventory(self):

        self.inventory_visible = not self.inventory_visible

    def draw_inventory(self, inventory):

        if not self.inventory_visible:
            return

        # Inventory dimensions and position
        width, height = 400, 200
        x = self.display_w / 2 - width / 2
        y = self.display_h - height
        inventory_rect = pygame.Rect(x, y, width, height)

        # Draw the background and border
        pygame.draw.rect(self.display_surface, self.inventory_bg_color, inventory_rect)
        pygame.draw.rect(self.display_surface, self.inventory_border_color, inventory_rect, 4)

        # Render each item in the inventory
        margin = 10
        start_x = inventory_rect.x + margin
        start_y = inventory_rect.y + margin
        text_gap = 40

        for idx, item in enumerate(inventory):
            item_text = f"{idx + 1}. {item.name}"
            text_surface = self.font.render(item_text, True, self.text_color)
            self.display_surface.blit(text_surface, (start_x, start_y + idx * text_gap))
