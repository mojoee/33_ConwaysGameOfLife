# Example file showing a basic pygame "game loop"
import pygame
from sim import Sim
from config import Config
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# board = Board()
sim = Sim(Config.fieldSize, screen)
playing = True


while running:
    while playing:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = False
                if event.key == pygame.K_c:
                    sim = Sim(Config.fieldSize, screen)
                if event.key == pygame.K_g:
                    for tile in sim.field.sprites():
                        if random.random() < Config.thresh:
                            tile.awaken()
        sim.field.update(events)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        # board.draw(screen)
        sim.field.draw(screen)

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(Config.fps)  # limits FPS to 60

pygame.quit()