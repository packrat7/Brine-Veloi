import pygame
from pygame import mixer
from random import randint

mixer.init()

def PlaySound(SoundToPlay,Volume):
  # Loading the song 
  mixer.music.load(f"Sounds/{SoundToPlay}.mp3") 
    
  # Setting the volume 
  mixer.music.set_volume(Volume) 
    
  # Start playing the song 
  mixer.music.play() 

def StopSound():
  mixer.music.stop() 
    
class Obstacle():
    def __init__(self, position, texture, gameObject, FunctionOnHit = None):

        self.FunctionOnHit = FunctionOnHit

        self.gameObject = gameObject

        self.Surface = pygame.Surface((100, 100))
        self.rect = self.Surface.get_rect()
        self.backuprect = self.rect

        self.position = position

        self.image = gameObject.TerrainSprites[texture]

        self.rect.x = self.position[0] + (self.gameObject.screenDimensions[0] * (self.gameObject.gameCords[0]))
        self.rect.y = self.position[1] + (self.gameObject.screenDimensions[1] * (self.gameObject.gameCords[1]))

    def draw(self, screen):
      screen.blit(self.image, self.rect)

    def update(self,screen):
      self.rect.x = self.position[0] + (self.gameObject.screenDimensions[0] * (self.gameObject.gameCords[0]))
      self.rect.y = self.position[1] + (self.gameObject.screenDimensions[1] * (self.gameObject.gameCords[1]))

class Character():
  def __init__(self, position, gameObject):

    self.AnimInfo = {
      "Idle":[5,20],
      "Walk":[2,10],
    }

    self.gameObject = gameObject
    self.Grounded = False
    self.Flipped = False
    self.GroundedLastTick = False
    self.FlippedLastTick = False
    self.CanCollide = False
    self.MaxInputVelocity = 3
    self.MaxVelocity = 10

    self.Frame = 1
    self.AnimFrame = 1
    self.State = "Idle"

    self.gameObject.objects.append(self)

    self.image = pygame.image.load(f"Assets/Sprites/{self.State}/{self.Frame}.png")
    self.image = pygame.transform.scale(self.image, (50, 150))
    self.rect = self.image.get_rect(center = position)

    self.Backupimage = self.image
    self.direction = {'x':0, 'y':0}
    self.speed = 5

  def airVelocity(self,x,y):

    TERMINALVELOCITY = 6

    #SIMULATE PUSH#
    self.direction['x'] += x*0.01
    self.direction['y'] += y*0.01

    #SIMULATE DRAG#
    if self.direction['x'] > 0:
      self.direction['x'] /= 1.01
    if self.direction['x'] < 0:
      self.direction['x'] /= 1.01
    
    if self.direction['y'] > 0:
      self.direction['y'] /= 1.01
    elif self.direction['y'] < 0:
      self.direction['y'] /= 1.01

    #SIMULATE TERMINALVELOCITY#
    if self.direction['x'] > TERMINALVELOCITY:
      self.direction['x'] = TERMINALVELOCITY
    elif self.direction['x'] < -TERMINALVELOCITY:
      self.direction['x'] = -TERMINALVELOCITY
    
    if self.direction['y'] < -TERMINALVELOCITY:
      self.direction['y'] += -TERMINALVELOCITY
     
  def groundVelocity(self,x,y):

    TERMINALVELOCITY = 3

    #SIMULATE PUSH#
    self.direction['x'] += x
    self.direction['y'] += y+0.1

    #SIMULATE DRAG#
    if self.direction['x'] > 0:
      self.direction['x'] /= 1.5
    if self.direction['x'] < 0:
      self.direction['x'] /= 1.5
    
    if self.direction['y'] > 0:
      self.direction['y'] = 0
    elif self.direction['y'] < 0:
      self.direction['y'] /= 1.01

    #SIMULATE TERMINALVELOCITY#
    if self.direction['x'] > TERMINALVELOCITY:
      self.direction['x'] = TERMINALVELOCITY
    elif self.direction['x'] < -TERMINALVELOCITY:
      self.direction['x'] = -TERMINALVELOCITY
    
    if self.direction['y'] > TERMINALVELOCITY:
      self.direction['y'] = TERMINALVELOCITY
    elif self.direction['y'] < -TERMINALVELOCITY:
      self.direction['y'] = -TERMINALVELOCITY

  def input(self):
    keys = pygame.key.get_pressed()
    cvX,cvY = 0,0
    self.State = "Idle"
    if keys[pygame.K_w] and self.Grounded == True:
      self.direction['y'] = -3.5
      self.Grounded = False

    if keys[pygame.K_d]:
      cvX += 1
      self.Flipped = True
      self.State = "Walk"
    elif keys[pygame.K_a]:
      cvX -= 1
      self.Flipped = False
      self.State = "Walk"

    if self.Grounded == True:
      self.groundVelocity(cvX,cvY)
    else:
      self.airVelocity(cvX,cvY)

  def move(self):
    self.Grounded = False

    self.GroundedLastTick = self.Grounded
    self.FlippedLastTick = self.Flipped
    self.rect.centerx += self.direction['x']*self.speed
    self.collide('x')
    self.rect.centery += self.direction['y']*self.speed
    self.direction['y'] += 0.1
    self.collide('y')

    if self.rect.centerx > self.gameObject.screenDimensions[1]:
      self.gameObject.gameCords[0] -= 1
      self.rect.centerx -= self.gameObject.screenDimensions[1]
    elif self.rect.centerx < 0:
      self.gameObject.gameCords[0] += 1
      self.rect.centerx += self.gameObject.screenDimensions[1]

    if self.rect.y > self.gameObject.screenDimensions[1]:
      self.gameObject.Boat()

  def collide(self, direction):
    if direction == direction:
      for obstacle in self.gameObject.objects:
          if obstacle.rect.colliderect(self.rect) and obstacle != self:
            if self.direction[direction] > 0:
              if direction == 'x':
                self.rect.right = obstacle.rect.left
              else:
                self.rect.bottom = obstacle.rect.top
                self.Grounded = True
            elif self.direction[direction] < 0:
              if direction == 'x':
                self.rect.left = obstacle.rect.right
              else:
                self.rect.top = obstacle.rect.bottom
            self.direction[direction] = 0
      for obstacle in self.gameObject.interactables:
          if obstacle.rect.colliderect(self.rect):
            if obstacle.FunctionOnHit != None:
              obstacle.FunctionOnHit(obstacle)

  def animate(self):
    self.Frame += 1
    if self.Frame > self.AnimInfo[self.State][1]:
      self.Frame = 1
      self.AnimFrame += 1
    if self.AnimFrame > self.AnimInfo[self.State][0]:
      self.AnimFrame = 1
    self.image = pygame.image.load(f"Assets/Sprites/{self.State}/{self.AnimFrame}.png")
    self.image = pygame.transform.scale(self.image, (92, 148))
    self.Backupimage = self.image

    self.image = pygame.transform.flip(self.Backupimage,self.Flipped,False)

  def draw(self,screen):
    screen.blit(self.image,(self.rect.x - (self.rect.width/2),self.rect.y))

  def update(self,event):
    self.input()
    self.move()
    self.animate()

class Button():
  def __init__(self, x, y, width, height, FunctionOnClick):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    
    self.FunctionOnClick = FunctionOnClick

    self.buttonSurface = pygame.Surface((self.width, self.height))
    self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    self.fillColors = {
        'normal': '#ffffff',
        'hover': '#666666',
        'pressed': '#333333' }

    self.alreadyPressed = False

  def draw(self, screen):
    self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
    screen.blit(self.buttonSurface, self.buttonRect)

  def update(self, event):
    mousePos = pygame.mouse.get_pos()
    self.buttonSurface.fill(self.fillColors['normal'])
    if self.buttonRect.collidepoint(mousePos):
      self.buttonSurface.fill(self.fillColors['hover'])
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        self.buttonSurface.fill(self.fillColors['pressed'])
        if not self.alreadyPressed:
            self.FunctionOnClick()
            self.alreadyPressed = True
      else:
          self.alreadyPressed = False

class Text_Button(Button):
  def __init__(self, x, y, width, height, FunctionOnClick, ButtonText="Placeholder"):
    super().__init__(x, y, width, height,FunctionOnClick)

    self.ButtonText = ButtonText

    self.Font = pygame.font.Font('freesansbold.ttf', height - 1)
    
    self.Text = self.Font.render(self.ButtonText, True, (255,255,255))

    self.TextBox = self.Text.get_rect(center = (self.x,self.y))

    self.fillColors = {
      'normal': '#ffffff',
      'hover': '#666666',
      'pressed': '#333333' }

  def draw(self, screen):
    self.buttonRect = pygame.Rect(self.x-(self.width/2), self.y-(self.height/2), self.width, self.height)
    #screen.blit(self.buttonSurface, self.buttonRect)
    screen.blit(self.Text, (self.TextBox.x, self.TextBox.y))
    

  def update(self, event):
    mousePos = pygame.mouse.get_pos()
    self.Text = self.Font.render(self.ButtonText, True, self.fillColors['normal'])
    if self.buttonRect.collidepoint(mousePos):
      self.Text = self.Font.render(self.ButtonText, True, self.fillColors['hover'])
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        self.Text = self.Font.render(self.ButtonText, True, self.fillColors['pressed'])
        if not self.alreadyPressed:
            self.FunctionOnClick()
            self.alreadyPressed = True
      else:
          self.alreadyPressed = False

class Text(Button):
  def __init__(self, x, y, width, height, ButtonText="Placeholder"):
    super().__init__(x, y, width, height,"None")

    self.ButtonText = ButtonText

    self.Font = pygame.font.Font('freesansbold.ttf', height - 1)

    self.Text = self.Font.render(self.ButtonText, True, (255,255,255))

    self.TextBox = self.Text.get_rect(center = (self.x,self.y))

    self.fillColors = {
      'normal': '#039dfc',
      'hover': '#004f80',
      'pressed': '#002c47' }

  def draw(self, screen):
      #self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
      #screen.blit(self.buttonSurface, self.buttonRect)
      screen.blit(self.Text, (self.TextBox.x, self.TextBox.y))

  def update(self, event):
    pass