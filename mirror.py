import random, sys, time, math, pygame
from pygame.locals import *

FPS = 60 # frames per second to update the screen
WINWIDTH = 640 # width of the program's window, in pixels
WINHEIGHT = 480 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

GRASSCOLOR = (24, 255, 0)
WHITE = (255, 255, 255,125)
RED = (255, 0, 0)
BLACK=(0,0,0,255)

CAMERASLACK = 90     # how far from the center the squirrel moves before moving the camera
MOVERATE = 9         # how fast the player moves
BOUNCERATE = 6       # how fast the player bounces (large is slower)
BOUNCEHEIGHT = 30    # how high the player bounces
STARTSIZE = 25       # how big the player starts off
WINSIZE = 300        # how big the player needs to be to win
INVULNTIME = 2       # how long the player is invulnerable after being hit in seconds
GAMEOVERTIME = 4     # how long the "game over" text stays on the screen in seconds
MAXHEALTH = 3        # how much health the player starts with

NUMGRASS = 80        # number of grass objects in the active area
NUMSQUIRRELS = 30    # number of squirrels in the active area
SQUIRRELMINSPEED = 3 # slowest squirrel speed
SQUIRRELMAXSPEED = 7 # fastest squirrel speed
DIRCHANGEFREQ = 2    # % chance of direction change per frame
LEFT = 'left'
RIGHT = 'right'

class Attack():
    def __init__(self):
        self.begintime=time.time()
        
        
class AttackLaser(Attack):
    def __init__(self,objID,direction,startpoint):
        Attack.__init__(self)
        self.rate=300
        self.objID=objID
        self.direction=direction
        self.startpoint=startpoint
        self.headpoint=self.startpoint
        self.attackObjs=[]
    def blit(self):
        deltatime=time.time()-self.begintime
        if(deltatime<0.2):
            startpoint=self.startpoint
        else:
            x= self.startpoint[0] - (deltatime-0.2)*self.rate*math.sin(math.radians(self.direction))
            y= self.startpoint[1] - (deltatime-0.2)*self.rate*math.cos(math.radians(self.direction))
            startpoint=(x,y)
        ex = startpoint[0] - 0.2*self.rate*math.sin(math.radians(self.direction))
        ey = startpoint[1] - 0.2*self.rate*math.cos(math.radians(self.direction))
        self.tailpoint=startpoint
        self.headpoint=(ex,ey)
        pygame.draw.line(DISPLAYSURF, (255,0,0,125), startpoint,(ex,ey),2)
        


class LaserPlane():
    def __init__(self,x=100,y=100,rotate=0,direction=0):
        self.img=pygame.Surface((50,50)).convert_alpha()
##        self.img=pygame.image.load('LaserPlane.bmp')
        self.x=float(x)
        self.y=float(y)
        self.rate=1
        self.turnrate=1
        self.direction=0
        self.layser=[]
        self.helth=200
        self.qcooldown = time.time()
#        pygame.Surface.convert_alpha(self.img)
        self.img.fill((255,255,255,0))
        pygame.draw.circle(self.img,BLACK,(25,25),25,3)
        pygame.draw.polygon(self.img,BLACK,((0,25),(25,0),(50,25)),3)
        if(len(PLANEID)==0):
            PLANEID.append(0)
            self.ID=0
        else:
            self.ID=PLANEID[-1]+1   
            PLANEID.append(self.ID)
        
        
    def blit(self):
        imgrotated=pygame.transform.rotate(self.img,self.direction)
        
        h=imgrotated.get_height()
        delta=(h-50)/2
        self.layserSkill()
        pixObj = pygame.PixelArray(imgrotated)
        for x in range(0,imgrotated.get_size()[0]):
            for y in range(0,imgrotated.get_size()[1]):
     #           a=pixObj[x][y][0:3]+pixObj[x][y][3]
                if (pixObj[x][y] != imgrotated.map_rgb((255, 255, 255,0))):
 #               i=(255,0,0,int(10*self.helth/100))
                    if(self.helth<100):
                        self.helth=0
                    pixObj[x][y]=(0,0,0,int(255*self.helth/200))
        #    i = (255,255,0,0)
        del pixObj
        DISPLAYSURF.blit(imgrotated, (self.x-delta,self.y-delta))
#        DISPLAYSURF.blit(self.imgrotated, (self.x,self.y))


        
        
    def turndirection(self,direction):
        if(direction=='left'):
            self.direction+=self.turnrate
        elif(direction=='right'):
            self.direction-=self.turnrate
    def setdirection(self,direction):
        self.direction=direction
    def push(self,direction='forward',):
        if(direction=='forward'):
            self.x-=self.rate*math.sin(math.radians(self.direction))
            self.y-=self.rate*math.cos(math.radians(self.direction))
        elif(direction=='backward'):
            self.x+=self.rate*math.sin(math.radians(self.direction))
            self.y+=self.rate*math.cos(math.radians(self.direction))
    def input(self,keyboardmap,keyboard={},mouse={}):
        if(keyboard[keyboardmap['left']]!=0):
            self.turndirection(LEFT)
        elif(keyboard[keyboardmap['right']]!=0 ):
            self.turndirection(RIGHT)
        if(keyboard[keyboardmap['up']]!=0):
            self.push('forward')
        elif(keyboard[keyboardmap['down']]!=0 ):
            self.push('backward')
        if(keyboard[keyboardmap['q']]!=0):
            if(time.time()-self.qcooldown>1):
                self.qcooldown = time.time()
                self.layserSkillAttack()
        
    def layserSkill(self):
        for i in self.layser:
            damage(i,PLANESET)
            i.blit()
        return
    def layserSkillAttack(self):
        x=self.x+25
        y=self.y+25
    
##        x+=25*math.cos(math.radians(self.direction-270))
##        y+=25*math.sin(math.radians(self.direction-270))
        self.layser.append(AttackLaser(self.ID,self.direction,(x,y)))

def collide(dam,obj):
    if((dam[0]-obj[0])**2+(dam[0]-obj[0])**2<25**2):
        return True
    else:
        return False
            
def damage(dams,objs):
    for i in objs:
        if (i.ID!=dams.objID):
            if(collide(dams.headpoint,(i.x,i.y))):
                i.helth-=1
    return
    


def keyboardinput(events,r):
    for event in events:
        if event.type == KEYDOWN:
            if event.key ==K_UP:
                r[K_DOWN]=0
                r[K_UP]=1
            if event.key==K_DOWN:
                r[K_DOWN]=1
                r[K_UP]=0
            if event.key==K_LEFT:
                r[K_LEFT]=1
                r[K_RIGHT]=0
            if event.key==K_RIGHT:
                r[K_LEFT]=0
                r[K_RIGHT]=1
            if event.key==K_w:
                r[K_w]=1
                r[K_s]=0
            if event.key==K_s:
                r[K_w]=0
                r[K_s]=1
            if event.key==K_a:
                r[K_a]=1
                r[K_d]=0
            if event.key==K_d:
                r[K_a]=0
                r[K_d]=1
            if event.key==K_q:
                r[K_q]=1
                
            
            if event.key==K_u:
                r[K_u]=1
            if event.key==K_i:
                r[K_i]=1
                r[K_k]=0
            if event.key==K_k:
                r[K_i]=0
                r[K_k]=1
            if event.key==K_j:
                r[K_j]=1
                r[K_l]=0
            if event.key==K_l:
                r[K_j]=0
                r[K_l]=1

        elif event.type == KEYUP:
                r[event.key]=0
    return r
def mouseinput(events):
    return


pygame.init()
FPSCLOCK = pygame.time.Clock()
global DISPLAYSURF,PLANEID,PLANESET
PLANEID=[]
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)

pygame.display.set_caption('Animation')

##anosurf=pygame.Surface((50,50))
##anosurf.fill(WHITE)
##pygame.draw.circle(anosurf,BLACK,(25,25),25,3)
cr={}
for i in range(0,500):
    cr[i]=0
PLANESET=[]
PLANESET.append(LaserPlane(random.randint(100,540),random.randint(100,380)))
PLANESET.append(LaserPlane(random.randint(100,540),random.randint(100,380)))

keyboardmap1={'left':K_j,'right':K_l,'up':K_i,'down':K_k,'q':K_u}
keyboardmap2={'left':K_a,'right':K_d,'up':K_w,'down':K_s,'q':K_q}
while True:
    DISPLAYSURF.fill(WHITE)
#    laserplane.push()
##    pygame.draw.circle(anosurf,WHITE,(25,25),25,3)
##    pygame.draw.polygon(anosurf,WHITE,((0,25),(25,0),(50,25)),3)
##    DISPLAYSURF.blit(anosurf, (200,200))

##    DISPLAYSURF.blit(pygame.transform.rotate(anosurf,45),(250,250))
    for i in PLANESET:
        i.blit()
    events=pygame.event.get()
    r=keyboardinput(events,cr)
#    print(r)
    PLANESET[0].input(keyboardmap1,r,{})
    PLANESET[1].input(keyboardmap2,r,{})
    for event in events:
            if event.type ==QUIT:
                    pygame.quit()
                    sys.exit()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
