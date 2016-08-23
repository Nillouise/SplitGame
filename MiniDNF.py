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
    ins = []
    def __init__(self, x=0, y=0, direction=LEFT):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.width = 50
        self.height = 110
        self.thickness = 20
        self.color = PLAYER_COLOR

        self.helth =200
        self.maxhelth = 200

        self.run_speedx = 500/FPS
        self.run_speedy = 110/FPS
        self.walk_speedx = 200/FPS
        self.walk_speedy = 110/FPS

        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)

        RedEye.ins.append(self)

    def input(self,vertical=0,horizon=0):
        if(horizon!=0):
            if(horizon>0):
                self.x += self.walk_speedx
                self.direction = RIGHT
            else:
                self.x -= self.walk_speedx
                self.direction = LEFT

        if(vertical!=0):
            if(vertical>0):
                self.y += self.walk_speedy
            else:
                self.y -= self.walk_speedy
        self.x,self.y = correctborder(self.x,self.y,0,WINWIDTH,0,WINHEIGHT)

    def paint(self):
        self.img.fill(self.color)
        #draw the direction
        if(self.direction == LEFT):
            pygame.draw.rect(self.img, (0, 255, 0, 255), (0, self.height*0.5 -15 , 10, 30 ), 0)
        else:
            pygame.draw.rect(self.img, (0, 255, 0, 255),(self.width - 10, self.height * 0.5 - 15, 10, 30), 0)
        #draw the helth
        pygame.draw.rect(self.img, (0, 255, 0, 255), (0, 0, self.width * self.helth / self.maxhelth, 8), 0)

    def skillX(self):
        SkillX(self.x,self.y-80,self.direction)


    @staticmethod
    def blitAll():
        for i in RedEye.ins:
            i.paint()
            DISPLAYSURF.blit(i.img, (i.x, i.y - i.height))


class SkillX():
    img = pygame.image.load("skillX.jpg")
    ins = []
    lasttime = 0
    def __init__(self,x,y,direction):
        if(time.time() - SkillX.lasttime >0.7):
            SkillX.lasttime = time.time()
        else:
            return
        self.x = x
        self.y = y

        self.width = 50
        self.height = 50
        self.thickness = 35

        self.speedx = 400/FPS
        self.direction = direction

        self.field = 130


        if(direction == RIGHT):
            self.targetx = x + self.field
        else:
            self.targetx = x - self.field
        self.targety = self.y
        self.targetx,self.targety = correctborder(self.targetx,self.targety,0,WINWIDTH,0,WINHEIGHT)

        self.attackmon = []
        SkillX.ins.append(self)

    def execute(self):
        if (self.direction == RIGHT):
            if(self.x>self.targetx ):
                SkillX.ins.pop()
            else:
                self.x += self.speedx
        else:
            if(self.x<self.targetx ):
                SkillX.ins.pop()
            else:
               self.x -=self.speedx


    def paint(self):
        self.img = SkillX.img

    def  collide(self):
        sk =  pygame.Rect(self.x,self.y,self.width,self.thickness)

        for i in MonMelee.ins:
            mon = pygame.Rect(i.x,i.y,i.width,i.thickness)
            rect = sk.clip(mon)
            if( rect.width != 0 and rect.height != 0 ):
                if(i not in self.attackmon):
                    self.attackmon.append(i)
                    i.helth -=30



        pass

    @staticmethod
    def blitAll():
        for i in SkillX.ins:
            i.paint()
            DISPLAYSURF.blit(i.img, (i.x, i.y))

    @staticmethod
    def executeAll():
        for i in SkillX.ins:
            i.execute()

    @staticmethod
    def collideAll():
        for i in SkillX.ins:
            i.collide()


def correctborder(x,y,borderx1,borderx2,bordery1,bordery2):
    if (x < borderx1):
        x = borderx1
    elif (x > borderx2):
        x = borderx2
    if (y < bordery1):
        y=bordery1
    elif(y>bordery2):
        y=bordery2
    return x,y

def linedirect(p1,p2):
    if(p1<p2):
        return 1
    else:
        return -1


class MonMelee():
    ins = []
    def __init__(self, x=0, y=0, direction=LEFT):

        self.x = float(x)
        self.y = float(y)

        self.width = 50
        self.height = 110
        self.thickness = 20
        self.color = MonMelee_COLOR

        self.run_speedx = 500
        self.run_speedy = 110
        self.walk_speedx = 200 / FPS
        self.walk_speedy = 110 / FPS

        self.maxhelth = 150
        self.helth = 150

        self.img = pygame.Surface((self.width, self.height)).convert_alpha()
        self.img.fill(self.color)

        self.targetx = -1
        self.targety = -1
        self.centerx = -1
        self.centery = -1

        self.staretime = 0

        MonMelee.ins .append(self)

    def round(self):
        if(self.centerx == -1):
            self.centerx = self.x + random.randint(-80,80)
            self.centery = self.y +random.randint(-50,50)
            self.centerx,self.centery = correctborder(self.centerx,self.centery,0,WINWIDTH,0,WINHEIGHT)
        elif(self.targetx == -1):
            self.targetx = self.centerx + random.randint(-80,80)
            self.targety = self.centery + random.randint(-50,50)
            self.targetx,self.targety = correctborder(self.targetx,self.targety,0,WINWIDTH,0,WINHEIGHT)
        elif(self.targetx == self.x and self.targety == self.y):
            self.targetx = self.centerx + random.randint(-80,80)
            self.targety = self.centery + random.randint(-50,50)
            self.targetx,self.targety = correctborder(self.targetx,self.targety,0,WINWIDTH,0,WINHEIGHT)
        else:
            if(abs(self.x - self.targetx)<self.walk_speedx ):
                self.x = self.targetx
            else:
                self.x = self.x+ linedirect(self.x,self.targetx)*self.walk_speedx

            if(abs(self.y - self.targety) <self.walk_speedy):
                self.y = self.targety
            else:
                self.y = self.y +linedirect(self.y,self.targety)*self.walk_speedy

            self.x,self.y = correctborder(self.x,self.y,0,WINWIDTH,0,WINHEIGHT)

    def attack(self):
        play = getPlayer()
        if(abs(self.y - play.y)<100):
            if(abs(self.x-play.x)<120):
                self.staretime += random.randint(40, 60) / FPS
            elif(abs(self.x - play.x)<500):
                self.staretime += random.randint(20,40)/FPS
            else:
                self.staretime *=0.995
        if(self.staretime > 110):
            play.helth-=30 #damage the player
            self.staretime = 0
            if(linedirect(play.x,self.x)==1):
                play.direction = RIGHT
            else:
                play.direction = LEFT


    def paint(self):
        self.img.fill(self.color)
        pygame.draw.rect(self.img, (0, 255, 0, 255), (0, 0, self.width * self.helth / self.maxhelth, 8), 0)

    @staticmethod
    def blitAll():
        for i in MonMelee.ins:
            i.paint()
            DISPLAYSURF.blit(i.img, (i.x, i.y - i.height))

    @staticmethod
    def attackAll():
        for i in MonMelee.ins:
            i.attack()

    @staticmethod
    def roundAll():
        for i in MonMelee.ins:
            i.round()


def getPlayer():
    return player




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

    def paint(self):
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
            elif(event.key==K_x):
                getPlayer().skillX()

        elif(event.type == KEYUP):
            if (event.key == K_UP):
                vertical = 0
            elif (event.key == K_DOWN):
                vertical = 0
            if (event.key == K_LEFT):
                horizon = 0
            elif (event.key == K_RIGHT):
                horizon = 0
    getPlayer().input(vertical,horizon)







pygame.init()
FPSCLOCK = pygame.time.Clock()

global DISPLAYSURF
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)
pygame.display.set_caption('MiniDNF')

global player
player = RedEye()

MonMelee(400,400)
MonMelee(500,300)

while True:
    DISPLAYSURF.fill(WHITE)

    events = pygame.event.get()
    keyboardinput(events)
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()




    SkillX.executeAll()
    SkillX.collideAll()
    SkillX.blitAll()

    RedEye.blitAll()

    MonMelee.roundAll()
    MonMelee.attackAll()
    MonMelee.blitAll()

    pygame.display.update()
    FPSCLOCK.tick(FPS)
