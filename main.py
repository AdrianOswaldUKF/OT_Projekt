from main_menu import MainMenu
import pygame

if __name__ == '__main__':

    pygame.init()

    display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Main menu
    menu = MainMenu()
    game = menu.run()

    game.run()
