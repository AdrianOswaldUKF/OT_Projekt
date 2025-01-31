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
        health_bar = max(0, min(current_health / max_health, 1))

        # Background
        pygame.draw.rect(self.display_surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(self.display_surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=10)

        # Color based on health
        health_color = (int(255 * (1 - health_bar)), int(255 * health_bar), 0)
        pygame.draw.rect(self.display_surface, health_color, (bar_x, bar_y, bar_width * health_bar, bar_height),
                         border_radius=10)

    def draw_health_text(self, current_health):

        health_text = f'Health: {current_health}'
        text_surface = self.font.render(health_text, True, (0, 0, 0))
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
                text_rect = text_surface.get_rect(center=(pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 - 100))
                self.display_surface.blit(text_surface, text_rect)
            else:

                self.pickup_message = ""

class InventoryGUI(GUI):

    def __init__(self, screen, player):
        super().__init__(screen, player)

        # Inventory UI settings
        self.inventory_bg_color = (50, 50, 50)
        self.inventory_border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 24)
        self.selected_item_index = 0

        self.equip_cooldown = PLAYER_INVENTORY_EQUIP_COOLDOWN
        self.mouse_equip_cooldown = PLAYER_INVENTORY_MOUSE_EQUIP_COOLDOWN

        self.last_equipped_time = 0
        self.last_mouse_equipped_time = 0

        # Initialize sword slots
        self.sword_slots = []

    def draw_toolbar(self):
        sword_rect_width = 48
        sword_rect_height = 48
        slot_spacing = 10
        start_x = pygame.display.Info().current_w // 2 - (sword_rect_width * 5 + slot_spacing * 4) // 2
        start_y = pygame.display.Info().current_h - sword_rect_height - 10

        self.sword_slots.clear()

        for i in range(5):
            sword_rect_x = start_x + i * (sword_rect_width + slot_spacing)
            sword_rect = pygame.Rect(sword_rect_x, start_y, sword_rect_width, sword_rect_height)
            self.sword_slots.append(sword_rect)  # Store the rect for each slot

            pygame.draw.rect(self.display_surface, (60, 60, 60), sword_rect, border_radius=12)
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

    def handle_mouse_input(self, mouse_pos, player):

        mouse_x, mouse_y = mouse_pos
        current_time = pygame.time.get_ticks()


        for idx, sword_rect in enumerate(self.sword_slots):

            if sword_rect.collidepoint(mouse_x, mouse_y):

                if pygame.mouse.get_pressed()[0]:

                    if current_time - self.last_mouse_equipped_time >= self.mouse_equip_cooldown:

                        if 0 <= idx < len(player.inventory):

                            item = player.inventory[idx]
                            player.equip_item(item)
                            self.selected_item_index = idx
                            self.last_mouse_equipped_time = current_time

                break

