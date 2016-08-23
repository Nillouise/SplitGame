import random, sys, time, math, pygame
from pygame.locals import *

FPS = 60  # frames per second to update the screen
WINWIDTH = 800  # width of the program's window, in pixels
WINHEIGHT = 600  # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

GRASSCOLOR = (24, 255, 0)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)
YELLOW = (255, 255, 0)

BLACK = (0, 0, 0, 255)

LEFT = 0
RIGHT = 1

PLAYER_COLOR = (255, 0, 0, 255)
MonMelee_COLOR = (140,140,0,255)
MonRemote_COLOR = (0,140,140,255)
MonBoss_COLOR = (0,255,255,255)
Obstacle_COLOR = (100,100,100,255)

AXIS_x1 = 287
AXIS_x2 = 367
AXIS_y1 = 349
AXIS_y2 = 449





class RedEye():
    def __init__(self, x=0, y=0, direction=LEFT):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.width = 50
        self.height = 110
        self.thickness = 20
        self.color = PLAYER_COLOR

        self.run_speedx = 500/FPS
        self.run_speedy = 110/FPS
        self.walk_speedx = 200/FPS
        self.walk_speedy = 110/FPS

        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)

    def input(self,vertical=0,horizon=0):
        if(horizon!=0):
            if(horizon>0):
                self.x += self.walk_speedx
            else:
                self.x -= self.walk_speedx

        if(vertical!=0):
            if(vertical>0):
                self.y += self.walk_speedy
            else:
                self.y -= self.walk_speedy



class MonMelee():
    def __init__(self, x=0, y=0, direction=LEFT):

        self.x = float(x)
        self.y = float(y)
        self.patrol = 1

        self.direction = direction
        self.width = 50
        self.height = 110
        self.thickness = 20
        self.color = MonMelee_COLOR

        self.run_speedx = 500
        self.run_speedy = 110
        self.walk_speedx = 200 / FPS
        self.walk_speedy = 110 / FPS
        self.helth = 150

        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)

        self.fieldx = 150
        self.fieldy = 100

        self.state = statePatrol(self,self.x,self.y,self.fieldx,self.fieldy)


class statePatrol():
    def __init__(self,mon,x,y,fieldx,fieldy):
        self.beginx = x
        self.beginy = y
        self.mon = mon
        self.fieldx = fieldx
        self.fieldy = fieldy

        self.endx = 0
        self.endy=0



    def findplayer(self):
        if(abs(obset[0].x - self.mon.x)<self.fieldx and (abs(obset[0].y-self.mon.y)<self.fieldy)):
            return True
        else:
            return False


    def execute(self):
        if(self.findplayer()):
            self.mon.state = stateAttack()
        else:
            if(self.endx != 0):
                self.run()
            else:
                self.endx = self.beginx +self.mon.walk_speedx*FPS*2
                self.endy = self.beginy +self.mon.walk_speedy*FPS*2
                self.run()

        return 0

    def run(self):
        if(self.mon.patrol != 0):
            x = self.mon.x +self.mon.walk_speedx
        else:
            x = self.mon.x - self.mon.walk_speedx


        if (x>self.endx ):
            self.mon.patrol = 0
        elif(x<self.beginx):
            self.mon.patrol = 1
        else:
            self.mon.x=x

        if(self.mon.patrol != 0):
            y = self.mon.y +self.mon.walk_speedy
        else:
            y = self.mon.y - self.mon.walk_speedy



        self.mon.y=y


class stateAttack():
    def __init__(self):
        pass



class MonRemote():
    def __init__(self, x=0, y=0, direction=LEFT):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.width = 50
        self.height = 110
        self.thickness = 20
        self.color = MonRemote_COLOR
        self.helth = 120
        self.run_speedx = 500
        self.run_speedy = 110
        self.walk_speedx = 200
        self.walk_speedy = 110
        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)


class MonBoss():
    def __init__(self, x=0, y=0, direction=LEFT):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.width = 50
        self.height = 110
        self.thickness = 20
        self.color = MonBoss_COLOR
        self.helth = 300

        self.run_speedx = 500
        self.run_speedy = 110
        self.walk_speedx = 200
        self.walk_speedy = 110
        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)




class Obstacle():
    def __init__(self, x=0, y=0,width = 50,hegiht=110,thickness=20):
        self.x = float(x)
        self.y = float(y)
        self.color = Obstacle_COLOR

        self.width = width
        self.height = hegiht
        self.thickness = thickness

        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)




def biltAll(a):
    for i in a:
        DISPLAYSURF.blit(i.img, (i.x, i.y))


pygame.init()
FPSCLOCK = pygame.time.Clock()

global DISPLAYSURF
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)
pygame.display.set_caption('MiniDNF')

global obset
obset = []
obset.append(RedEye())
obset.append(MonMelee(300,100))
obset.append(MonRemote(120,120))
obset.append(MonBoss(200,200))
obset.append(Obstacle(300,300))
global horizon,vertical
horizon = 0
vertical = 0
def keyboardinput(events):
    global horizon,vertical
    for event in events:
        if(event.type==KEYDOWN):
            if(event.key == K_UP):
                vertical = -1
            elif(event.key==K_DOWN):
                vertical = 1
            if(event.key == K_LEFT):
                horizon=-1
            elif(event.key == K_RIGHT):
                horizon = 1
        elif(event.type == KEYUP):
            if (event.key == K_UP):
                vertical = 0
            elif (event.key == K_DOWN):
                vertical = 0
            if (event.key == K_LEFT):
                horizon = 0
            elif (event.key == K_RIGHT):
                horizon = 0
    obset[0].input(vertical,horizon)

while True:
    DISPLAYSURF.fill(WHITE)

    obset[1].state.execute()
    biltAll(obset)


    events = pygame.event.get()
    keyboardinput(events)
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    FPSCLOCK.tick(FPS)
