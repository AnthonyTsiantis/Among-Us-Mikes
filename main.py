# Import libraries
import pygame, sys

# Inilitize pygame
pygame.init()

# Create game caption
pygame.display.set_caption("St. Mike's Among Us!")

# Initilize main clock
mainClock = pygame.time.Clock()


# Create the screen (Ajusts to computers screen size)
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

# Create fullscreen boolean
fullscreen = False




# Main loop
while True:

    # Fill the screen
    screen.fill((0, 255, 255))

    # Event listener for loop
    for event in pygame.event.get():
        
        # Quit program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # resize to screen dimensions
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # key down
        if event.type == pygame.KEYDOWN:
            # maps F11 key to fullscreen
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                
                # Updates display to fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)
                
                else: 
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

    # Updates display loop and main clock
    pygame.display.update()
    mainClock.tick(60)

