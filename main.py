import pygame
import sys

from menu import Menu
from constants import *
from game import Game


def main():

    # ----------------------------------------
    # Initialize Pygame
    # ----------------------------------------

    pygame.init()

    pygame.display.set_caption("Python Chess")

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    clock = pygame.time.Clock()

    # ----------------------------------------
    # Create Game
    # ----------------------------------------

    menu = Menu()

    print(menu.is_solo())
    print(menu.play_white)

    in_menu = True

    # ----------------------------------------
    # Main Loop
    # ----------------------------------------

    running = True

    while running:

        clock.tick(FPS)

        # ------------------------------------
        # Events
        # ------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif in_menu:

                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):

                    menu.mouse_down(event.pos)

            else:

                game.handle_event(event)

        # ------------------------------------
        # Menu
        # ------------------------------------

        if in_menu:

            menu.update()

            menu.draw(screen)

            if menu.is_finished():

                game = Game(

                    solo=menu.is_solo(),

                    player_is_white=menu.play_white

                )

                in_menu = False

        # ------------------------------------
        # Game
        # ------------------------------------

        else:

            game.update()

            game.draw(screen)

        pygame.display.flip()

    # ----------------------------------------
    # Quit
    # ----------------------------------------

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()