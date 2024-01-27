import sys
import pygame
import Levels
from random import randint
from Classes import Button, Text_Button, Text, Character, Obstacle, PlaySound, StopSound

BLACK = (0, 0, 0)

class Game():
  def __init__(self):

    self.Money = 0
    self.Haul = 0
    self.Rent = 0
    self.Day = 0

    self.player = 0

    self.Level = 0

    self.Levels = [
      Levels.Reef,
      Levels.Trench,
      Levels.Abyss
    ]

    self.TerrainSprites = [
      pygame.image.load(f"Assets/Sprites/Sand.png"),
      pygame.image.load(f"Assets/Sprites/Treasure.png"),
      pygame.image.load(f"Assets/Sprites/Finish.png"),
      pygame.image.load(f"Assets/Sprites/MainScreen.png"),

      pygame.image.load(f"Assets/Sprites/Reef.jpg"),
      pygame.image.load(f"Assets/Sprites/Trench.jpg"),
      pygame.image.load(f"Assets/Sprites/Abyss.jpg")
    ]
    
    self.gameCords = [0,0]

    self.screenDimensions = [800,800]
    self.screen = pygame.display.set_mode((self.screenDimensions[0],self.screenDimensions[1]))
    self.clock = pygame.time.Clock()
    self.FPS = 60
    
    self.objects = []
    self.interactables = []
    self.ui = []

  def GameTick(self,event):

    #LOGIC

    for object in self.objects:
      object.update(event)

    for object in self.interactables:
      object.update(event)

    for object in self.ui:
      object.update(event)

    #VISUALIZE

    self.screen.fill((14,31,37))

    for object in self.objects:
      object.draw(self.screen)

    for object in self.interactables:
      object.draw(self.screen)

    for object in self.ui:
      object.draw(self.screen)

    pygame.display.update()
    self.clock.tick(self.FPS)
      
  def LevelRight(self):
    self.Level += 1
    if self.Level > 2:
      self.Level = 0
    self.ui = self.ui[:-2]
    self.ui.append(Obstacle((225,250), self.Level + 4, self))
    self.ui.append(Text(400,575, 150, 15,f"Level {self.Level + 1}"))
  
  def LevelLeft(self):
    self.Level -= 1
    if self.Level < 0:
      self.Level = 2
    self.ui = self.ui[:-2]
    self.ui.append(Obstacle((225,250), self.Level + 4, self))
    self.ui.append(Text(400,575, 150, 15,f"Level {self.Level + 1}"))

  def Collect(self,object):
    self.Haul += 10
    self.interactables.remove(object)
    PlaySound("MoneyCollect",1)

  def Surface(self,object):
    self.interactables = []
    self.objects = []
    self.ui = []
    self.gameCords = [0,0]

    self.Money += self.Haul
    print(self.Money)
    self.Money -= self.Rent
    print(self.Money)

    self.ui.append(Text(400, 250, 150, 40,f"Haul: {self.Haul}"))

    self.ui.append(Text(400, 15, 150, 15,"Haul Result"))

    if self.Money >= 0:
      PlaySound("Win",1)
      self.ui.append(Text(400, 200, 150, 40,f"You were able to pay your ${self.Rent} rent!"))

      self.ui.append(Text(400, 300, 150, 40,f"Rent: {self.Rent} (Payed)"))
      self.ui.append(Text(400, 350, 150, 40,f"Money Left In Bank: {self.Money}"))

      self.ui.append(Text_Button(400, 700, 150, 40,self.Boat,"Return To Boat"))
    else:
      PlaySound("Fail",1)
      self.ui.append(Text(400, 200, 150, 40,f"You weren't able to pay your rent..."))
      
      self.ui.append(Text(400, 300, 150, 40,f"Rent: {self.Rent} (Unpayed)"))
      self.ui.append(Text(400, 350, 150, 40,f"Money Left In Bank: {self.Money} (You're broke!)"))

      self.ui.append(Text_Button(400, 700, 150, 40,self.InitMenu,"End Game"))

  def InitMenu(self):

    self.Money = 0
    self.Haul = 0
    self.Rent = 0
    self.Day = 0

    self.player = 0

    self.Level = 0

    self.objects = []
    self.interactables = []
    self.ui = []
    self.gameCords = [0,0]

    self.ui.append(Obstacle((0,100), 3, self))

    self.ui.append(Text(400, 140, 150, 120,"Brine:Veloi"))
    self.ui.append(Text_Button(400, 700, 150, 50,self.Boat,"Start Game"))

  def Boat(self):
    StopSound()
    self.Rent += 10 * self.Day
    self.Haul = 0

    self.interactables = []
    self.objects = []
    self.ui = []
    self.gameCords = [0,0]

    self.ui.append(Text(400, 15, 150, 15,"The Boat"))
    self.ui.append(Text(400, 40, 150, 15,f"Day {self.Day}"))
    self.ui.append(Text(400, 140, 150, 80,f"Bank: ${self.Money}"))
    self.ui.append(Text(400, 200, 150, 60,f"Rent: ${self.Rent}"))

    self.ui.append(Text_Button(400, 650, 150, 40,self.Ocean,"Start Diving"))

    self.ui.append(Text_Button(200, 400, 50, 20,self.LevelLeft,"<<"))
    self.ui.append(Text_Button(600, 400, 50, 20,self.LevelRight,">>"))

    #Tip

    Tips = [
      "Make Blood Sacrificed to improve your peformance",
      "Taking a running start is required for certain jumps",
      "Dying is bad",
      "Be careful when entering the next area, there may be a hole ahead you cant see"
    ]

    self.ui.append(Text(400, 750, 150, 15,f"TIP: {Tips[randint(0,len(Tips))-1]}"))

    self.ui.append(Obstacle((225,250), self.Level + 4, self))
    self.ui.append(Text(400,575, 150, 15,f"Level {self.Level + 1}"))

  def Ocean(self):
    StopSound()

    self.Day += 1

    self.interactables = []
    self.objects = []
    self.ui = []
    self.gameCords = [0,0]

    tilemakerposition = [0,0]

    for List in self.Levels[self.Level]:
      for value in List:
        if value == "G":
          self.objects.append(Obstacle((100 * tilemakerposition[0],100 * tilemakerposition[1]), 0, self))
        elif value == "E":
          self.interactables.append(Obstacle((100 * tilemakerposition[0],100 * tilemakerposition[1]), 2, self, self.Surface))
        elif value == "$":
          self.interactables.append(Obstacle((100 * tilemakerposition[0],100 * tilemakerposition[1]), 1, self, self.Collect))
        tilemakerposition[0] += 1
      tilemakerposition[0] = 0
      tilemakerposition[1] += 1

    self.player = Character((400,400) ,self)