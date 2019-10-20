import random, pygame, sys
import math
from pygame.locals import *

pygame.font.init()
inta = 0
lastevent = 't'
RES = (900, 600)
disp = pygame.display.set_mode(RES)
pygame.display.set_caption('hey')
menudisp = pygame.Surface(RES)
FPS = 30
FPSCLOCK = pygame.time.Clock()
mouseState = []
for i in range(0, 10): mouseState.append(False)

class board:
    boardDisp = pygame.Surface(RES)
    keyState = 0

    def __init__(self, wid = 30, hi = 16, min = 10):
        assert(min < wid * hi), print('more mines than tiles')
        self.tiles = []
        self.mines = min
        self.initted = False
        self.state = 0
        for w in range(wid):
            self.tiles.append([])
            for h in range(hi):
                self.tiles[w].append([0, False, False])


    def neighbours(self, x, y):
        ret = []
        l = x > 0
        r = x < len(self.tiles) - 1
        u = y > 0
        d = y < len(self.tiles[0]) - 1
        if (l): ret.append((x - 1, y))
        if (l and u): ret.append((x - 1, y - 1))
        if (l and d): ret.append((x - 1, y + 1))
        if (r): ret.append((x + 1, y))
        if (r and u): ret.append((x + 1, y - 1))
        if (r and d): ret.append((x + 1, y + 1))
        if (u): ret.append((x, y - 1))
        if (d): ret.append((x, y + 1))
        return ret

    def draw(self):
        self.boxSize = int(min((RES[0] - 50)/ len(self.tiles), (RES[1] - 50)/ len(self.tiles[0])))
        myFont = pygame.font.SysFont('arial', int(self.boxSize - 5))
        #print(self.boxSize)
        assert self.boxSize > 16, print('too many boxes for the window')
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[0])):
                # tileColor = (255, 0, 0) if self.tiles[x][y][0] == -1  else (0, 255, 0)
                # img = 'mine.png' if self.tiles[x][y][0] == -1 and self.lost == True else 'tile.png'
                #print(img)
                #print(str(25 + (x * self.boxSize)), str(25 + (y * self.boxSize)))
                if(self.tiles[x][y][1] and self.tiles[x][y][0] != -1):
                    pygame.draw.rect(self.boardDisp, (150, 150, 150), (25 + (x * self.boxSize), 25 + (y * self.boxSize), self.boxSize, self.boxSize))
                    if(self.tiles[x][y][0] != 0): self.boardDisp.blit(myFont.render(str(self.tiles[x][y][0]), False, (0, 0, 0)), (27 + (x * self.boxSize), 27 + (y * self.boxSize)))
                else:
                    self.boardDisp.blit(pygame.transform.scale(pygame.image.load('tile.png'), (int(self.boxSize), int(self.boxSize))), (25 + (x * self.boxSize), 25 + (y * self.boxSize)))
                    if self.tiles[x][y][0] == -1 and self.state == -1 and not self.tiles[x][y][2]: self.boardDisp.blit(pygame.transform.scale(pygame.image.load('mine.png'), (int(self.boxSize), int(self.boxSize))), (25 + (x * self.boxSize), 25 + (y * self.boxSize)))
                    if self.tiles[x][y][2] == True: self.boardDisp.blit(pygame.transform.scale(pygame.image.load('flag.png'), (int(self.boxSize), int(self.boxSize))), (25 + (x * self.boxSize), 25 + (y * self.boxSize)))
                #pygame.draw.rect(self.boardDisp, tileColor, (25 + (x * self.boxSize), 25 + (y * self.boxSize), self.boxSize - 5, self.boxSize - 5))
                #print('drawn')
        #pygame.draw.rect(self.boardDisp, (0, 255, 0), (0, 0, 200, 200))
        face = 'surprised.png' if mouseState[1] else 'happy.png'
        if(self.state == -1): face = 'dead.png'
        if(self.state == 1): face = 'sunglasses.png'
        self.boardDisp.blit(pygame.transform.scale(pygame.image.load(face), (25, 25)), (RES[0] / 2 - 25, 0))
        disp.blit(self.boardDisp, (0, 0))
        #print('t')

    def findBox(self, coords):
        ret = (math.trunc((coords[0] - 25) / self.boxSize), math.trunc((coords[1] - 25) / self.boxSize))
        return ret

    def click(self, coords, mode):
        #print(str(coords))
        if(mode == 1):
            if(not self.initted):
                self.addMines(self.mines, coords)
                self.initted = True
            if self.tiles[coords[0]][coords[1]][1] == True: return()
            if self.tiles[coords[0]][coords[1]][0] == -1 and self.state == 0: self.state = -1
            if self.state == -1: return()
            self.tiles[coords[0]][coords[1]][1] = True
            if(self.tiles[coords[0]][coords[1]][0] == 0):
                #print('clickin')
                for j in self.neighbours(coords[0], coords[1]): self.click(j, 1)
        if(mode == 3):
            self.tiles[coords[0]][coords[1]][2] = not self.tiles[coords[0]][coords[1]][2]
        counta = 0
        for i in range(0, len(self.tiles)):
            for j in range(0, len(self.tiles[0])):
              if(not(self.tiles[i][j][1]) and self.tiles[i][j][0] != -1):
                  counta += 1
        if(counta == 0):
            self.state = 1
            for i in range(0, len(self.tiles)):
                for j in range(0, len(self.tiles[0])):
                    if (self.tiles[i][j][0] == -1):
                        self.tiles[i][j][2] = True


    def processClick(self, event):
        if (25 <= event.pos[0] <= (self.boxSize * (len(self.tiles) + 1)) and 25 <= event.pos[1] <= (
                self.boxSize * (len(self.tiles[0]) + 1))):
            self.click(game.findBox(event.pos), event.button)
        if(RES[0] / 2 - 25 <= event.pos[0] <= RES[0] / 2 and event.pos[1] <= 25):
            self.__init__()
        #self.boardDisp.blit(pygame.transform.scale(pygame.image.load(face), (25, 25)), (RES[0] / 2 - 25, 0))


    def addMines(self, min, coords):
        while(min > 0):
            spot = random.randint(0, len(self.tiles) * len(self.tiles[0]) - 1)
            spotx = spot % len(self.tiles)
            spoty = math.trunc(spot / len(self.tiles))
            if(not((self.tiles[spotx][spoty][0] == -1) or spotx == coords[0] or spoty == coords[1])):
                self.tiles[spotx][spoty][0] = -1
                neighbourl = self.neighbours(spotx, spoty)
                for tile in neighbourl:
                    if(not(self.tiles[tile[0]][tile[1]][0] == -1)): self.tiles[tile[0]][tile[1]][0] += 1
                min -= 1

game = board()
while True:
    lastint = inta
    for event in pygame.event.get():
        if event == lastevent and inta == lastint: break
        if event.type == QUIT:
            pygame.quit()
            sys.exit('h')
        if event.type == MOUSEBUTTONDOWN:
            mouseState[event.button] = True
        if event.type == MOUSEBUTTONUP:
            #print(event)
            #print(str(event.pos))
            mouseState[event.button] = False
            game.processClick(event)
            print(game.state)
        lastevent = event
    inta += 1
    game.draw()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    #print('e')
