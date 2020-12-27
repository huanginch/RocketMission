#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pygame


# In[2]:


import sys

import random
import pygame
from pygame.locals import QUIT,USEREVENT


# In[3]:


#定義顏色
Yellow = (255,255,0)
Black = (0,0,0)
White = (255,255,255)
Blue = (61,89,171)
#定義視窗大小
window_width = 1000
window_height = 600
#定義隕石圖片大小
IMAGEWIDTH = 50
IMAGEHEIGHT = 50
#Rocket初始參數
rt_x = 550
rt_y = 250
rt_dx = 1.5
rt_dy = 1.5

#分數
score=0
#分數座標
score_x=853
score_y=0

#燃料包與隕石群組
FuelPacks_list = pygame.sprite.Group()
Meteorite_list = pygame.sprite.Group()

clock = pygame.time.Clock()
FPS = 60


# In[4]:


#初始化
pygame.init()
#視窗大小為window_width，window_height
windows_surface = pygame.display.set_mode((window_width,window_height)) 
#載入Rocket.png
rocket_image = [pygame.image.load('RocketL.png').convert_alpha(),
            pygame.image.load('RocketR.png').convert_alpha(),
            pygame.image.load('RocketU.png').convert_alpha(),
            pygame.image.load('RocketD.png').convert_alpha()]
meteorite_image = ["stoneU.png", 
               "stoneD.png", 
               "stoneL.png", 
               "stoneR.png"]

#畫面標題RocketMission
pygame.display.set_caption('RocketMission') 
#背景大小為視窗大小
background = pygame.Surface(windows_surface.get_size()) 
#增加繪製速度
background.convert() 
#從(0,0)填入背景
windows_surface.blit(background, (0,0))

#匯入字體
arial_s = pygame.font.SysFont("arial", 20)
arial = pygame.font.SysFont("arial", 40)
arial_L = pygame.font.SysFont("arial", 100)


# In[5]:


#PacMan物件
class Rocket(pygame.sprite.Sprite):
    def __init__(self,x,dx,y,dy):
        super().__init__()
        self.image = rocket_image[0]
        #回傳位置
        self.rect = self.image.get_rect() 
        #定位
        self.rect.center = (x,y)
        self.x = rt_x
        self.y = rt_y
        self.dx = rt_dx
        self.dy = rt_dy
        
    def draw(self,ws):
        
        ws.blit(self.image, (self.x,self.y)) #從(x,y)填入PacMan.jpg
        
    
    #左移
    def moveL(self):
        if self.x > 0: 
            self.image = rocket_image[0]
            self.x -= self.dx
        
    #右移
    def moveR(self):
        if self.x < window_width-75: 
            self.image = rocket_image[1]
            self.x += self.dx
        
    #上移
    def moveU(self):
        if self.y > 0: 
            self.image = rocket_image[2]
            self.y -= self.dy
       
    #下移
    def moveD(self):
        if self.y < window_height-75:
            self.image = rocket_image[3]
            self.y += self.dy


# In[6]:


#燃料包物件
class FuelPack(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        #載入fuelpack
        self.image = pygame.image.load('fuelpack.png').convert_alpha()
        #回傳位置   
        self.rect = self.image.get_rect() 


# In[7]:


#隕石物件
class Meteorite(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, widow_width, window_height, index):
        super().__init__()
        self.raw_image = pygame.image.load(meteorite_image[index]).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = width
        self.height = height
        self.widow_width = widow_width
        self.window_height = window_height
        self.index = index
    def move(self, x, y, index):
        if(index == 0):
            y -= 50
        elif(index == 1):
            y += 50
        elif(index == 2):
            x -= 50
        else:
            x += 50
        if(x < 0):
            x += window_width
        elif(x > window_width):
            x %= window_width
        if(y < 0):
            y += window_height
        elif(y > window_height):
            y %= window_height
        return x, y
    def turn(self, meteorite, index):
        row1 = pygame.Rect(0, 200, 500, 15)
        row2 = pygame.Rect(500, 400, 500, 15)
        col1 = pygame.Rect(250, 0, 15, 1000)
        col2 = pygame.Rect(500, 0, 15, 1000)
        col3 = pygame.Rect(750, 0, 15, 1000)
        if(pygame.Rect.colliderect(row1, meteorite.rect) or pygame.Rect.colliderect(row2, meteorite.rect) or            pygame.Rect.colliderect(col1, meteorite.rect) or (pygame.Rect.colliderect(col2, meteorite.rect) or            pygame.Rect.colliderect(col3, meteorite.rect))):
            index = random.randint(0,3)
        return index
    def wall_collision_detect(self, meteorite, x, y, index):
        wall_top = pygame.Rect(0, 10, 1000, 4)
        wall_bottom = pygame.Rect(0, 580, 1000, 4)
        wall_left = pygame.Rect(15, 0, 10, 600)
        wall_right = pygame.Rect(980, 0, 10, 600)
        if(pygame.Rect.colliderect(wall_top, meteorite.rect)):
            #print("ohhhhh")
            index = 1
            x, y = meteorite.move(x, y, index)
        elif(pygame.Rect.colliderect(wall_bottom, meteorite.rect)):
            index = 0
            x, y = meteorite.move(x, y, index)
        elif(pygame.Rect.colliderect(wall_left, meteorite.rect)):
            index = 3
            x, y = meteorite.move(x, y, index)
        elif(pygame.Rect.colliderect(wall_right, meteorite.rect)):
            index = 2
            x, y = meteorite.move(x, y, index)
        return x, y, index


# In[8]:


#創建地圖
def createMap():

    bg_image=pygame.image.load('Background.jpg').convert()
    windows_surface.blit(bg_image,(0,0))
    
    #顯示分數
    score_surface = arial.render("score:%d" %score, True, White, Blue)
    windows_surface.blit(score_surface, (score_x, score_y))
    
    #少於10個再創建新的fuelpack
    if len(FuelPacks_list)<10:
        createFuelPack()


# In[9]:


#畫燃料包
def createFuelPack():
    for i in range(35):
        
        #創建燃料包物件
        fp=FuelPack(10,10)
        
        #為燃料包設定一個隨機座標
        fp.rect.x=random.randrange(0,850)
        fp.rect.y=random.randrange(42,window_height-75)

        #加入群組
        FuelPacks_list.add(fp)


# In[10]:


#創建隕石
def createMeteorite():
    x, y = 965,465   #1st隕石的起始位置
    index = 0
    meteorite = Meteorite(IMAGEWIDTH, IMAGEHEIGHT, x, y, window_width, window_height, index) #1st meteorite initialize
    x2, y2 = 215, 215  #2nd隕石的起始位置
    index2 = 3
    meteorite2 = Meteorite(IMAGEWIDTH, IMAGEHEIGHT, x2, y2, window_width, window_height, index2)
    
    Meteorite_list.add(meteorite)
    Meteorite_list.add(meteorite2)


# In[11]:


#移動隕石
def reloadMeteorite():
    
    for meteorite in Meteorite_list:

        x, y = meteorite.move(meteorite.rect.x,meteorite.rect.y,meteorite.index)            
        index = meteorite.turn(meteorite, meteorite.index)
        x, y,index = meteorite.wall_collision_detect(meteorite,x, y,index)
        new_meteorite = Meteorite(IMAGEWIDTH, IMAGEHEIGHT, x, y, window_width, window_height, index)
        Meteorite_list.remove(meteorite)
        Meteorite_list.add(new_meteorite)


# In[12]:


def playBGM():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(20)
    pygame.mixer.music.load("through_the_space.mp3")
    pygame.mixer.music.play()


# In[13]:


def playgameover():
    pygame.mixer.music.load("through_the_space.mp3")
    pygame.mixer.music.play()


# In[14]:


#創建PRocket
Rocket = Rocket(rt_x,rt_dx,rt_y,rt_dy)


# In[15]:


#創建fuelpack
createFuelPack()


# In[16]:


#創建meteorite
createMeteorite()


# In[17]:


reload_ghost_event = USEREVENT + 1
pygame.time.set_timer(reload_ghost_event, 300)

GameOver=False


# In[18]:


#main loop

playBGM()
run = True
while run:
    clock.tick(FPS)
    #關閉視窗
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == reload_ghost_event:
            reloadMeteorite()
    #背景黑色
    background.fill(Black) 

    createMap()

    keys = pygame.key.get_pressed()

    #鍵盤控制PacMan移動
    if keys[pygame.K_w]:
            Rocket.moveU()
    if keys[pygame.K_a]:
            Rocket.moveL()
    if keys[pygame.K_s]:
            Rocket.moveD()
    if keys[pygame.K_d]:
            Rocket.moveR()


    #偵測碰撞FuelPack
    for fp in FuelPacks_list:
        if fp.rect.collidepoint(Rocket.x+25,Rocket.y+25):
            score += 1
            FuelPacks_list.remove(fp)

    #偵測碰撞Meteorite
    for meteorite in Meteorite_list:
        if meteorite.rect.collidepoint(Rocket.x+25,Rocket.y+25):
            pygame.mixer.music.unload()
            playgameover()
            GameOver=True

    if not GameOver:
        #畫出燃料包
        FuelPacks_list.draw(windows_surface)

        #畫出隕石
        Meteorite_list.draw(windows_surface)

        #繪製 Rocket
        Rocket.draw(windows_surface)
    else:
        windows_surface.fill(Black)
        gameover = arial_L.render("GameOver", True, White, Black)
        yourscore = arial.render("Your score:%d"%score, True, White, Black)
        playagain = arial.render("Press space to play again", True, White, Black)
        windows_surface.blit(gameover, (280, 200))
        windows_surface.blit(yourscore, (395, 310))
        windows_surface.blit(playagain, (300, 350))
        if keys[pygame.K_SPACE]:
            playBGM()
            score=0
            GameOver=False

    pygame.display.update()    

pygame.quit()        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




