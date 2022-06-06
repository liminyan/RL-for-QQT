import pygame,sys,time
from pygame.locals import *
from sys import exit
import numpy as np
import Player 
import config
import Boom
import AI
import Env

X,Y = 800,600
Player_size = 40

me = Player.Player('liminyan',Player_size,X,Y )

global_BoomQueue = Boom.BoomQueue(X,Y,Player_size)
global_player = []
global_player.append(me)

# global_player.append(AI.AI_Player('AI0',Player_size,X,Y,'r'))
# global_player.append(AI.AI_Player('AI1',Player_size,X,Y,'r'))
# global_player.append(AI.AI_Player('AI2',Player_size,X,Y,'r'))
# global_player.append(AI.AI_Player('AI3',Player_size,X,Y,'r') )
# global_player.append(AI.AI_Player('AI4',Player_size,X,Y,'r'))
# global_player.append(AI.AI_Player('AI5',Player_size,X,Y,'r'))
# global_player.append(AI.AI_Player('AI6',Player_size,X,Y,'r'))

config.set_global_BoomQueue(global_BoomQueue)
config.set_global_player(global_player)
config.set_boom_color((0, 255, 0))
config.set_bar_color((0,0,255))

pygame.init()
screen = pygame.display.set_mode((X,Y),0,30) #主界面 
config.set_screen(screen)
env = Env.Env(global_player,global_BoomQueue,screen)


while True: #main loop
    env.generate_view(Player_size,X,Y)
    # if env.end():
    #     print('end!')
        # env.reset()
   






