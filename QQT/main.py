import pygame,sys,time
from pygame.locals import *
from sys import exit
import numpy as np
import Player 
import config
import Boom
import AI

X,Y = 800,600
Player_size = 30

me = Player.Player('liminyan',Player_size,X,Y )

global_BoomQueue = Boom.BoomQueue(X,Y,Player_size)
global_player = []
global_player.append(me)

global_player.append(AI.AI_Player('AI0',Player_size,X,Y,'r'))
global_player.append(AI.AI_Player('AI1',Player_size,X,Y,'r'))
global_player.append(AI.AI_Player('AI2',Player_size,X,Y,'r'))
global_player.append(AI.AI_Player('AI3',Player_size,X,Y,'r'))
global_player.append(AI.AI_Player('AI4',Player_size,X,Y,'r'))
global_player.append(AI.AI_Player('AI5',Player_size,X,Y,'r'))
global_player.append(AI.AI_Player('AI6',Player_size,X,Y,'r'))

config.set_global_BoomQueue(global_BoomQueue)
config.set_global_player(global_player)
config.set_boom_color((0, 255, 0))
config.set_bar_color((0,0,255))

pygame.init()
screen = pygame.display.set_mode((X,Y),0,30) #主界面
config.set_screen(screen)

while True: #main loop
    for event in pygame.event.get():#获取事件
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    for player in global_player:
        player.move()
        player.DrawPlayer(screen)

    global_BoomQueue.update()
    global_BoomQueue.DrawBooml(screen)
    global_BoomQueue.check_player(screen)
    pygame.display.update()

