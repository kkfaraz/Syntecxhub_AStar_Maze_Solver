import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
win = pygame.display.set_mode((800, 800))
win.fill((255, 0, 0))
pygame.image.save(win, "test_dummy.png")
print("Saved")
