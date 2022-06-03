import numpy as np
import pygame,sys,time
import Boom
import config


class Move(object):
    """docstring for Move"""
    def __init__(self):
        super(Move, self).__init__()
        self.map_key = {}
        self.map_key[pygame.K_RIGHT]= np.array([-1,0])
        self.map_key[pygame.K_DOWN] = np.array([0,-1])
        self.map_key[pygame.K_LEFT] = np.array([1,0])
        self.map_key[pygame.K_UP] = np.array([0,1])
    def move(self,key,prox):
        return self.map_key[key] * prox.speed

class Prox(object):
    """docstring for Prox"""
    def __init__(self):
        super(Prox, self).__init__()
        self.speed = 6.5
        self.power = 2
        self.state = '0'
        self.boom_num = 0
        self.max_boom_num = 4


class Player(object):
    """docstr ing for Player"""
    def __init__(self, name,Player_size,X,Y ):
        super(Player, self).__init__()
        self.name = name
        self.Move = Move()
        self.Prox = Prox()
        self.x,self.y = 0,0
        self.show_name = True
        self.Player_size = Player_size
        self.center_x = self.x+len(self.name)*2+Player_size/2
        self.center_y = self.y+20+Player_size/2
        self.state = 'Move'
        self.bias = ''
        self.X = X
        self.Y = Y


    def move(self):

        if self.state == "Dead" :
            self.bias ='[Dead]'

        keys=pygame.key.get_pressed()
        if(keys[pygame.K_RIGHT] == True):
            op = self.Move.move(pygame.K_RIGHT,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(keys[pygame.K_DOWN] == True):
            op = self.Move.move(pygame.K_DOWN,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(keys[pygame.K_UP] == True):
            op = self.Move.move(pygame.K_UP,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(keys[pygame.K_LEFT] == True):
            op = self.Move.move(pygame.K_LEFT,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(keys[pygame.K_RETURN] == True):
            tex = pygame.font.SysFont('宋体',size = 25)
            tex_fmt = tex.render('[!]',1,'white')
            config.get_screen().blit(tex_fmt,(self.x + self.Player_size/2,self.y - self.Player_size/2))

        self.x = max(0,self.x)
        self.y = max(0,self.y)

        self.x = min(self.X-20 -self.Player_size ,self.x)
        self.y = min(self.Y-20 -self.Player_size,self.y)

        self.center_x = self.x+len(self.name)*2+self.Player_size/2
        self.center_y = self.y+20+self.Player_size/2

        if(keys[pygame.K_SPACE] == True) and self.state == 'Move' :
            if self.Prox.boom_num < self.Prox.max_boom_num :
                self.state = 'Boom'
                self.Prox.boom_num += 1
                curBoom = Boom.Boom(self.center_x,self.center_y,self)
                self.Attack(curBoom)

        if self.state == 'Boom' and (keys[pygame.K_SPACE] == False):
            self.state = 'Move'

    def DrawPlayer(self,screen):

        if self.show_name:
            tex = pygame.font.SysFont('宋体',size = 25)
            tex_fmt = tex.render(self.name+self.bias,1,'white')
            screen.blit(tex_fmt,(self.x,self.y))

        mycolcor = (0, 0, 255)
        position = ( self.x+len(self.name+self.bias)*2, self.y+20, self.Player_size, self.Player_size )
        
        width = 1
        pygame.draw.rect( screen, mycolcor, position, width )

        # print(self.center_x,self.center_y)

    def Attack(self,boom):
        config.get_global_BoomQueue().recive(boom)

