import pygame
import random

WIDTH = 640 # setting variables in the beginning
HEIGHT = 480 # this is a variable
FPS = 30 # unsurprisingly, this is a variable too

# Colors (remember, variables go at the top)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) #dabadee dabadaa, dabadee da ba daa
DISCO = (120, 255, 50)
#these lil dudes do nothing on their own, but we
pygame.init()
#and magic happens
pygame.mixer.init() # this one's for dank beats
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dongman 3:The return of the revenge")
clock = pygame.time.Clock() #more like cock amirite lmao

#anyway, here we be doin loop-de-loops
running_in_the_90s = True
while running_in_the_90s:
    # Keep the loop running
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running_in_the_90s = False
    # Update

    # Render
    screen.fill(DISCO)
    #afterwards, we flipp
    pygame.display.flip()

pygame.quit
