import pygame

from const import PLAYER_INVENTORY_EQUIP_COOLDOWN, PLAYER_INVENTORY_MOUSE_EQUIP_COOLDOWN


class GUI:

    def __init__(self, screen, player):

        self.display_surface = screen
        self.display_w = self.display_surface.get_width()
        self.display_h = self.display_surface.get_height()
        self.gui_surface = pygame.Surface(screen.get_size())
        self.font = pygame.font.Font(None, 36)
        self.player = player

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

    def __init__(self, screen, player):

        super().__init__(screen, player)

        # Inventory UI settings
        self.inventory_bg_color = (50, 50, 50)
        self.inventory_border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 24)
        self.inventory_visible = False
        self.selected_item_index = 0


        self.equip_cooldown = PLAYER_INVENTORY_EQUIP_COOLDOWN
        self.mouse_equip_cooldown = PLAYER_INVENTORY_MOUSE_EQUIP_COOLDOWN

        self.last_equipped_time = 0
        self.last_mouse_equipped_time = 0


    def toggle_inventory(self):

        self.inventory_visible = not self.inventory_visible

    def draw_inventory(self, inventory):

        if not self.inventory_visible:
            return

        width, height = 400, 200
        x = self.display_w / 2 - width / 2
        y = self.display_h - height
        inventory_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.display_surface, self.inventory_bg_color, inventory_rect)
        pygame.draw.rect(self.display_surface, self.inventory_border_color, inventory_rect, 4)

        margin = 20
        start_x = inventory_rect.x + margin
        start_y = inventory_rect.y + margin
        text_gap = 30

        for idx, item in enumerate(inventory):
            item_index = f"{idx + 1}"
            item_text = f'{item.name}'
            self.font.render(item_text, True, self.text_color)

            if item == self.player.equipped:

                pygame.draw.rect(self.display_surface, (0, 255, 0), pygame.Rect(start_x - 5, start_y + idx * text_gap - 5, 370, text_gap + 10))
                text_index_surface = self.font.render(item_index, True,(0, 0, 0))
                text_surface = self.font.render(item_text, True,(0, 0, 0))
            else:

                pygame.draw.rect(self.display_surface, self.inventory_bg_color, pygame.Rect(start_x - 5, start_y + idx * text_gap - 5, 370, text_gap + 10))
                text_index_surface = self.font.render(item_index, True, self.text_color)
                text_surface = self.font.render(item_text, True, self.text_color)

            self.display_surface.blit(text_index_surface, (start_x, start_y + idx * text_gap))
            self.display_surface.blit(text_surface, (start_x + 125, start_y + idx * text_gap))

            if hasattr(item, 'image'):
                self.display_surface.blit(item.image, (start_x + 340, start_y + idx * text_gap))

    def handle_input(self, player):

        keys = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        for i in range(1, 5 +1):

            if keys[getattr(pygame, f'K_{i}')]:

                item_index = i - 1

                if 0 <= item_index < len(player.inventory):
                    if current_time - self.last_equipped_time >= self.equip_cooldown:
                        selected_item = player.inventory[item_index]
                        player.equip_item(selected_item)
                        self.last_equipped_time = current_time
                    break

    def handle_mouse_input(self, mouse_pos, player, inventory):

        if not self.inventory_visible:
            return

        mouse_x, mouse_y = mouse_pos
        margin = 20
        start_x = self.display_w / 2 - 200
        start_y = self.display_h - 200

        current_time = pygame.time.get_ticks()

        for idx, item in enumerate(inventory):

            item_rect = pygame.Rect(start_x + margin, start_y + margin + idx * 30, 360, 30)

            if item_rect.collidepoint(mouse_x, mouse_y):

                if current_time - self.last_mouse_equipped_time >= self.mouse_equip_cooldown:
                    player.equip_item(item)
                    self.selected_item_index = idx
                    self.last_mouse_equipped_time = current_time
                break