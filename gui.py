import pygame

from const import PLAYER_INVENTORY_EQUIP_COOLDOWN, PLAYER_INVENTORY_MOUSE_EQUIP_COOLDOWN
from sword import Sword


class GUI:

    def __init__(self, screen, player):

        self.display_surface = screen
        self.gui_surface = pygame.Surface(screen.get_size())
        self.font = pygame.font.Font(None, 36)
        self.player = player

        self.pickup_message = ""
        self.pickup_timer = 0
        self.pickup_duration = 2000  # Show message for 2 seconds

    def draw_health_bar(self, current_health, max_health):

        # Dimensions
        bar_width = 300
        bar_height = 20
        bar_x = 20
        bar_y = 20

        # Health bar
        health_bar = current_health / max_health

        # Background
        pygame.draw.rect(self.display_surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(self.display_surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=10)

        health_color = (0, int(255 * (1 - health_bar)), int(255 * health_bar))
        pygame.draw.rect(self.display_surface, health_color, (bar_x, bar_y, bar_width * health_bar, bar_height), border_radius=10)

    def draw_health_text(self, current_health):

        health_text = f'Health: {current_health}'
        text_surface = self.font.render(health_text, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (20, 50))

    def draw_fps(self, current_fps):

        fps_text = f'FPS: {current_fps}'
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.display_surface.blit(fps_surface, (pygame.display.Info().current_w - 150, 10))

    def show_pickup_message(self, message):

        self.pickup_message = message
        self.pickup_timer = pygame.time.get_ticks()

    def draw_pickup_message(self):

        if self.pickup_message:

            elapsed_time = pygame.time.get_ticks() - self.pickup_timer

            if elapsed_time < self.pickup_duration:

                text_surface = self.font.render(self.pickup_message, True, (255, 255, 0))
                self.display_surface.blit(text_surface, (pygame.display.Info().current_w // 2 - 130, pygame.display.Info().current_h // 2 - 100))
            else:

                self.pickup_message = ""

    def draw_equipped_sword(self):

        sword_rect_width = 48
        sword_rect_height = 48
        slot_spacing = 10
        start_x = pygame.display.Info().current_w // 2 - (sword_rect_width * 5 + slot_spacing * 4) // 2
        start_y = pygame.display.Info().current_h - sword_rect_height - 10


        for i in range(5):

            sword_rect_x = start_x + i * (sword_rect_width + slot_spacing)
            sword_rect = pygame.Rect(sword_rect_x, start_y, sword_rect_width, sword_rect_height)

            # Background
            pygame.draw.rect(self.display_surface, (60, 60, 60), sword_rect, border_radius=12)

            # Border
            pygame.draw.rect(self.display_surface, (50, 50, 50), sword_rect, border_radius=12, width=3)

            if self.player.inventory and i < len(self.player.inventory):

                selected_sword = self.player.inventory[i]

                if isinstance(selected_sword, Sword):

                    if selected_sword == self.player.equipped:

                        pygame.draw.rect(self.display_surface, (0, 255, 0), sword_rect, border_radius=12, width=3)

                    if hasattr(selected_sword, 'image'):

                        sword_image = pygame.transform.scale(selected_sword.image,
                                                             (sword_rect.width, sword_rect.height))
                        self.display_surface.blit(sword_image, sword_rect.topleft)
                else:

                    pygame.draw.rect(self.display_surface, (30, 30, 30), sword_rect, border_radius=12)
            else:

                pygame.draw.rect(self.display_surface, (30, 30, 30), sword_rect, border_radius=12)


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
        x = pygame.display.Info().current_w / 2 - width / 2
        y = pygame.display.Info().current_h - height
        inventory_rect = pygame.Rect(x, y, width, height)

        # Background
        pygame.draw.rect(self.display_surface, (0, 0, 0), (inventory_rect.x, inventory_rect.y, width, height), border_radius=10)
        pygame.draw.rect(self.display_surface, (60, 60, 60), (inventory_rect.x, inventory_rect.y, width, height), border_radius=10)

        pygame.draw.rect(self.display_surface, self.inventory_border_color, inventory_rect, 4)

        margin = 20
        start_x = inventory_rect.x + margin
        start_y = inventory_rect.y + margin
        text_gap = 30

    def handle_input(self, player):

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        for i in range(1, 5 + 1):

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
        start_x = pygame.display.Info().current_w / 2 - 200
        start_y = pygame.display.Info().current_h - 200

        current_time = pygame.time.get_ticks()

        for idx, item in enumerate(inventory):

            item_rect = pygame.Rect(start_x + margin, start_y + margin + idx * 30, 360, 30)

            if item_rect.collidepoint(mouse_x, mouse_y):

                if current_time - self.last_mouse_equipped_time >= self.mouse_equip_cooldown:

                    player.equip_item(item)
                    self.selected_item_index = idx
                    self.last_mouse_equipped_time = current_time

                break
