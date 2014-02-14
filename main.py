#!/usr/bin/env python
import pygame
from pygame import *
from sys import exit
import random
from time import sleep
pygame.init()
screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption("FiappoCube!!")
clock=pygame.time.Clock()
update_set=pygame.sprite.Group()
time=0
walls=pygame.sprite.Group()
maluslist=pygame.sprite.Group()
text=pygame.font.SysFont("Arial",16)
GameOver=False
mode=1
gc=1
iteration=0
maltime=0.
gs=1
snd_fly=pygame.mixer.Sound("fly.wav")
snd_death=pygame.mixer.Sound("death.wav")
score=0
class Player (pygame.sprite.Sprite):
    movey=0
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,20))
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        update_set.add(self)
    def update(self):
        self.rect.y+=self.movey
        screen.blit(self.image,(self.rect.x,self.rect.y))
        collide=pygame.sprite.spritecollide(self,walls,False)
        if collide:
            self.kill()
            global GameOver
            GameOver=True
            snd_death.play()
        if self.rect.y<0 or self.rect.y>460:
            self.kill()
            global GameOver
            GameOver=True
            snd_death.play()
player=Player(100,100)
class WeightMalus(pygame.sprite.Sprite):
    def __init__(self,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=text.render(" W ",True,(255,255,0),(255,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=700
        self.rect.y=y
        update_set.add(self)
        maluslist.add(self)
    def update(self):
        self.rect.x-=5
        if self.rect.x<=-50:
            self.kill()
        screen.blit(self.image,(self.rect.x,self.rect.y))
        collide=pygame.sprite.spritecollide(player,maluslist,False)
        if collide:
            global gc
            gc=2
            self.kill()
class FloatMalus(pygame.sprite.Sprite):
    def __init__(self,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=text.render(" F ",True,(0,0,255),(255,255,0))
        self.rect=self.image.get_rect()
        self.rect.x=700
        self.rect.y=y
        update_set.add(self)
        maluslist.add(self)
    def update(self):
        self.rect.x-=5
        if self.rect.x<=-50:
            self.kill()
        screen.blit(self.image,(self.rect.x,self.rect.y))
        collide=pygame.sprite.spritecollide(player,maluslist,False)
        if collide:
            global gc
            gc=-1
            self.kill()
class SpeedMalus(pygame.sprite.Sprite):
    def __init__(self,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=text.render(" >> ",True,(0,0,255),(128,128,128))
        self.rect=self.image.get_rect()
        self.rect.x=700
        self.rect.y=y
        update_set.add(self)
        maluslist.add(self)
    def update(self):
        self.rect.x-=5
        if self.rect.x<=-50:
            self.kill()
        screen.blit(self.image,(self.rect.x,self.rect.y))
        collide=pygame.sprite.spritecollide(player,maluslist,False)
        if collide:
            global gs
            gs=2
            self.kill()
def generateMalus():
    spacestart=random.randint(100,300)
    decide=random.randint(0,2)
    if decide==0:
        for i in range(0,spacestart,30):
            WeightMalus(i)
        for i in range(spacestart+100,480,30):
            WeightMalus(i)
    elif decide==1:
        for i in range(0,spacestart,30):
            FloatMalus(i)
        for i in range(spacestart+100,480,30):
            FloatMalus(i)
    elif decide==2:
        for i in range(0,spacestart,30):
            SpeedMalus(i)
        for i in range(spacestart+100,480,30):
            SpeedMalus(i)
class Column(pygame.sprite.Sprite):
    passed=False
    def __init__(self,height):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((50,height))
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.x=700
        self.rect.y=480-height
        update_set.add(self)
        walls.add(self)
    def update(self):
        global gs
        self.rect.x-=5*gs
        screen.blit(self.image,(self.rect.x,self.rect.y))
        if self.rect.x<-50:
            self.kill()
        if not self.passed and not GameOver:
            if player.rect.x>self.rect.x:
                self.passed=True
                global score
                score+=1
class Column2(pygame.sprite.Sprite):
    def __init__(self,height):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((50,380-height))
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.x=700
        self.rect.y=0
        update_set.add(self)
        walls.add(self)
    def update(self):
        global gs
        self.rect.x-=5*gs
        screen.blit(self.image,(self.rect.x,self.rect.y))
        if self.rect.x<-50:
            self.kill()
def gravity():
    player.movey+=0.9*gc
sleep(5)
while True:
    screen.fill((0,0,0))
    gravity()
    global tp
    global mode
    global iteration
    global gc
    global gs
    if gc!=1:
        global maltime
        if maltime/1000.>=10:
            gc=1
            maltime=0
        else:
            maltime+=tp
    if gs!=1:
        global maltime
        if maltime/1000.>=10:
            gs=1
            maltime=0
        else:
            maltime+=tp
    if mode==1:
        global gs
        if time/1000.>=1*1/gs:
            time=0
            h=random.randint(100,300)
            Column(h)
            Column2(h)
            iteration+=1
        if iteration>=10:
            mode=2
            iteration=0
    elif mode==2:
        if time/1000.>=1:
            generateMalus()
            mode=1
            time=0
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        if event.type==KEYDOWN:
            if event.key==K_UP:
                player.movey=-1*random.randint(5,8)*(gc/abs(gc))
                snd_fly.play()
    for element in update_set:
        element.update()
    if GameOver:
        screen.blit(text.render("Game Over",True,(255,0,0)),(320,240))
    screen.blit(text.render("Score: {0}".format(score),True,(255,0,0)),(10,10))
    pygame.display.update()
    tp=clock.tick(30)
    time+=tp
