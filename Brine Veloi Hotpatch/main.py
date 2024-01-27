import game
import sys
import pygame

pygame.init()

pygame.display.set_caption("Brine:Veloi")
icon = pygame.image.load("Assets/Textures/Icon.png")
pygame.display.set_icon(icon)

GameClass = game.Game()

if __name__ ==  "__main__":
  GameClass.InitMenu()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    GameClass.GameTick(event)