import pygame
import gc
from loading_screen_file import loading_process

# pygame initialization
pygame.init()

# clock, framerate = 30 fps
clock = pygame.time.Clock()

# main function
def main():
    global clock

    # create window
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Anything")

    # creating a loading process
    loading_screen = loading_process(surface)

    # main loop
    run = True
    FPS = 30
    while run:
        # 30 fps
        clock.tick(FPS)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # loading animation
        loading_screen.create_loading_screen(8, FPS)  # (seconds, FPS)

        if loading_screen.check_if_still_loading():
            run = False

        # update window
        pygame.display.update()

    # releasing memory
    del loading_screen
    gc.collect()

    # After previous loop you can write another one here, you better make another loop because I released some memory deleting loading object

    # ---------------------------------------------------------------------

if __name__ == "__main__":
    # main function
    main()

    # deactivates the pygame library
    #pygame.quit()