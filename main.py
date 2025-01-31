from game import Game
from main_menu import MainMenu
import pygame

if __name__ == '__main__':
    pygame.init()

    # Set up the display surface (fullscreen or a specific resolution)
    display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Run the main menu, which will return the Game instance after 'Start' is clicked
    menu = MainMenu(display_surface)
    game = menu.run()  # Transition from main menu to the game

    # Now run the game
    game.run()
