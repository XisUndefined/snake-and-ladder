import sys, pygame, random, os
from spritesheet import Spritesheet

os.chdir(rf"{os.path.realpath(os.path.dirname(__file__))}")

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

icon = pygame.image.load("./icon.ico")
res_w, res_h = 1366, 768
screen = pygame.Surface((res_w, res_h))
window = pygame.display.set_mode((res_w, res_h))
caption = pygame.display.set_caption("Snake & Ladder")
pygame.display.set_icon(icon)

def playMusic(filename: str, loop: int):
  pygame.mixer.music.load(filename)
  return pygame.mixer.music.play(loop)

def pauseMusic(filename: str):
  pygame.mixer.music.load(filename)
  return pygame.mixer.music.pause()

gameClock = pygame.time.Clock()

p1 = pygame.image.load("data/images/Mario.png")
p2 = pygame.image.load("data/images/Luigi.png")
cpu = pygame.image.load("data/images/Yoshi.png")
p1_p2 = pygame.image.load("data/images/Mario & Luigi.png")
p1_cpu = pygame.image.load("data/images/Mario & Yoshi.png")
mainmenu = pygame.image.load("data/images/Ladder & Snake (Menu).png")
board = pygame.image.load("data/images/Ladder & Snake (Gameplay).png")
p1_win = pygame.image.load("data/images/Player 1 Win-1.png")
p2_win = pygame.image.load("data/images/Player 2 Win-2.png")
lose = pygame.image.load("data/images/You Lose.png")

for i in range(6):
  globals()[f"dice_{i+1}"] = Spritesheet(f"data/images/Roll Dice Sprite Sheet {i+1}.png")
  globals()[f"dice_{i+1}_list"] = []

for i in range(52):
  for j in range(6):
    globals()[f"dice_{j+1}_list"].append(globals()[f"dice_{j+1}"].parse_sprite(f"Roll_Dice 1_Artboard {i+1}.png"))

menuFont = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 20)
playerFont = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 40)
diceFont = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 45)
turnFont = pygame.font.Font('data/fonts/Super Mario Bros. 2.ttf', 20)

pos = [(1200, 624), (1200,504), (1200, 384), (1200,264), (1080,384), (960,384), (840,384), (840,264), (840,144)]
list_p = []
turn = 2
n, m, posChange, xn = 0, 0, 0, 0
back = False

class Player():
  def __init__(self, image, overlapImage):
    self.image = image
    self.overlapImage = overlapImage

  def draw(self, position):
    self.position = position
    self.rectImage = self.image.get_rect(center = self.position)
    self.rectOverlap = self.overlapImage.get_rect(center = self.position)
    if n == m:
      window.blit(self.overlapImage, self.rectOverlap)
    else:
      window.blit(self.image, self.rectImage)

class Button():
  def __init__(self, text: str, x: int, y: int, font):
    self.clicked = False
    self.textSurf = font.render(text, True, '#FFFFFF')
    self.textRect = self.textSurf.get_rect(center = (x, y))

  def draw(self):
    action = False
    mousePos = pygame.mouse.get_pos()
    if self.textRect.collidepoint(mousePos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True
    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False
    window.blit(self.textSurf, self.textRect)
    return action
  
singleButton = Button("Single Player", 683, 433, playerFont)
multiButton = Button("Multiplayer", 683, 513, playerFont)
diceButton = Button("Roll", 1165, 155, diceFont)

nextFrame = pygame.time.get_ticks()
diceFrame = pygame.time.get_ticks()
diceStatic, staticTime, frame, frameChange = 0, 0, 0, 0

def choosePlayer():
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if singleButton.draw() == True:
        player_1 = Player(p1, p1_cpu)
        com = Player(cpu, p1_cpu)
        list_p.append(player_1)
        list_p.append(com)
        gameloop1()
      if multiButton.draw() == True:
        player_1 = Player(p1, p1_p2)
        player_2 = Player(p2, p1_p2)
        list_p.append(player_1)
        list_p.append(player_2)
        gameloop2()
    window.blit(mainmenu, (0,0))
    singleButton.draw()
    multiButton.draw()
    pygame.display.update()
    gameClock.tick(50)

def menu():
  pauseMusic("data/sounds/gotcha.wav")
  pauseMusic("data/sounds/Level Complete.wav")
  playMusic("data/sounds/Theme Song.wav", -1)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0] == 1:
        choosePlayer()
    menuMsg = menuFont.render("Press Any Button to Start", True, WHITE)
    menuRect = menuMsg.get_rect(center = (683, 473))
    window.blit(mainmenu, (0, 0))
    window.blit(menuMsg, menuRect)
    pygame.display.update()
    gameClock.tick(50)

def winner(filename: str, player):
  global turn, n, m, list_p
  pauseMusic("data/sounds/Theme Song.wav")
  playMusic(filename, 0)
  turn = 3
  list_p = []
  n, m = 0, 0
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0] == 1:
        menu()
    window.blit(player, (0, 0))
    pygame.display.update()
    gameClock.tick(50)

def gameloop1():
  global n, m, nextFrame, frame, frameChange, staticTime, diceFrame, posChange, diceStatic, turn, xn, back
  numberOfDice = 0
  while True:
    window.blit(board, (0, 0))
    list_p[0].draw(pos[n])
    list_p[1].draw(pos[m])
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if diceButton.draw() == True and turn%2 == 0:
        staticTime = nextFrame
        numberOfDice = random.randint(1,6)
        frame = 0
        frameChange = 1
    if pygame.time.get_ticks() > nextFrame:
      frame = (frame + frameChange) % 52
      if frameChange == 1:
        nextFrame += 1
      if nextFrame - staticTime > 50 and frameChange == 1:
        frameChange = 0
        diceStatic = diceFrame
        posChange = 1
    if pygame.time.get_ticks() > diceFrame:
      if posChange == 1:
        diceFrame += 1
      if (diceFrame - diceStatic) % 5 == 0 and posChange == 1:
        if turn%2 == 0 and back == False:
          n += 1
          if n >= 9:
            back = True
        if turn%2 == 0 and back == True and n == 9:
          n = 8
        if turn%2 == 0 and back == True:
          n -= 1

        if turn%2 == 1 and back == False:
          m += 1
          if m >= 9:
            back = True
        if turn%2 == 1 and back == True and m == 9:
          m = 8
        if turn%2 == 1 and back == True:
          m -= 1
      if diceFrame - diceStatic > 5 * numberOfDice and posChange == 1:
        if numberOfDice != 6:
          turn += 1
        if n == 1:
          n += 4
        if m == 1:
          m + 4
        if n == 8:
          winner("data/sounds/Level Complete.wav", p1_win)
        if m == 8:
          winner("data/sounds/gotcha.wav", lose)
        posChange = 0
        back = False
        if turn%2 == 1:
          staticTime = nextFrame
          numberOfDice = random.randint(1,6)
          frame = 0
          frameChange = 1

    for dice in range(6):
      if numberOfDice == dice + 1:
        window.blit(globals()[f"dice_{dice+1}_list"][frame], (1020, 564))
      if numberOfDice == 0:
        window.blit(dice_1_list[frame], (1020, 564))
    diceButton.draw()
    
    if turn%2 == 0:
      p1Msg = turnFont.render("Player 1 Turn", True, BLACK)
      p1Rect = p1Msg.get_rect(center = (1125, 97))
      window.blit(p1Msg, p1Rect)
    if turn%2 == 1:
      cpuMsg = turnFont.render("CPU Turn", True, BLACK)
      cpuRect = cpuMsg.get_rect(center = (1175, 97))
      window.blit(cpuMsg, cpuRect)
    
    xn += 1
    pygame.display.update()
    gameClock.tick(50)

def gameloop2():
  global n, m, nextFrame, frame, frameChange, staticTime, diceFrame, posChange, diceStatic, turn, xn, back
  numberOfDice = 0
  while True:
    window.blit(board, (0,0))
    list_p[0].draw(pos[n])
    list_p[1].draw(pos[m])
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if diceButton.draw() == True:
        staticTime = nextFrame
        numberOfDice = random.randint(1,6)
        frame = 0
        frameChange = 1
    if pygame.time.get_ticks() > nextFrame:
      frame = (frame + frameChange) % 52
      if frameChange == 1:
        nextFrame += 1
      if nextFrame - staticTime > 50 and frameChange == 1:
        frameChange = 0
        diceStatic = diceFrame
        posChange = 1
    if pygame.time.get_ticks() > diceFrame:
      if posChange == 1:
        diceFrame += 1
      if (diceFrame - diceStatic) % 5 == 0 and posChange == 1:
        if turn%2 == 0 and back == False:
          n += 1
          if n >= 9:
            back = True
        if turn%2 == 0 and back == True and n == 9:
          n = 8
        if turn%2 == 0 and back == True:
          n -= 1
        
        if turn%2 == 1 and back == False:
          m += 1
          if m >= 9:
            back = True
        if turn%2 == 1 and back == True and m == 9:
          m = 8
        if turn%2 == 1 and back == True:
          m -= 1
      if diceFrame - diceStatic > 5 * numberOfDice and posChange == 1:
        if numberOfDice != 6:
          turn += 1
        if n == 1:
          n += 4
        if m == 1:
          m += 4
        if n == 8:
          winner("data/sounds/Level Complete.wav", p1_win)
        if m == 8:
          winner("data/sounds/Level Complete.wav", p2_win)
        posChange = 0
        back = False

    for dice in range(6):
      if numberOfDice == dice + 1:
        window.blit(globals()[f"dice_{dice+1}_list"][frame], (1020, 564))
      if numberOfDice == 0:
        window.blit(dice_1_list[frame], (1020, 564))
    diceButton.draw()

    if turn%2 == 0:
      p1Msg = turnFont.render("Player 1 Turn", True, BLACK)
      p1Rect = p1Msg.get_rect(center = (1125, 97))
      window.blit(p1Msg, p1Rect)
    if turn%2 == 1:
      p2Msg = turnFont.render("Player 2 Turn", True, BLACK)
      p2Rect = p2Msg.get_rect(center = (1125, 97))
      window.blit(p2Msg, p2Rect)
    
    xn += 1

    pygame.display.update()
    gameClock.tick(50)

if __name__ == "__main__":
  menu()