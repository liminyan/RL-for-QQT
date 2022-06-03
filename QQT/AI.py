import numpy as np
import Player
import pygame,time
import random
import Boom
import config
 
class AI_Player(object):
    """docstr ing for AI_Player"""
    def __init__(self, name,Player_size,X,Y ,mode = None):
        super(AI_Player, self).__init__()
        self.name = name
        self.Move = Player.Move()
        self.Prox = Player.Prox()
        self.X = X
        self.Y = Y

        if mode == None:
            self.x,self.y = 0,0
        if mode == 'r':
            self.x = random.randint(0,self.X-20 -Player_size)
            self.y = random.randint(0,self.Y-20 -Player_size)

        self.show_name = True
        self.Player_size = Player_size
        self.center_x = self.x+len(self.name)*2+Player_size/2
        self.center_y = self.y+20+Player_size/2
        self.state = 'Move'
        self.bias = ''
        self.first = time.time()
        self.space = time.time()
        self.key = 0

    def move(self):

        if self.state == "Dead" :
            self.bias ='[Dead]'
            return

        key = self.key
        if time.time() - self.first >=0.1:
	        key = random.randint(0,9)
	        self.first = time.time()

        STOP = True
        LEFT = False
        UP = False
        RIGHT = False
        DOWN = False
        SPACE = False

        if key == 0:
            STOP = True

        if key == 1:
            RIGHT = False
            LEFT = True
        if key == 2:
            DOWN = False
            UP = True

        if key == 3:
            RIGHT = True
        if key == 4:
            DOWN = True

        if key == 5:
            LEFT = True
            UP = True

        if key == 6:
            RIGHT = True
            DOWN = True

        if key == 7:
            RIGHT = True
            UP = True

        if key == 8:
            LEFT = True
            DOWN = True

        self.key = key
        if time.time() - self.space >=0.4 or key == 9:
	        key = random.randint(0,9)
	        self.space = time.time() 

        if key ==  9:
            SPACE = True
        # if STOP:
        #     return

       
        # keys=pygame.key.get_pressed()
        if(RIGHT == True):
            op = self.Move.move(pygame.K_RIGHT,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(DOWN == True):
            op = self.Move.move(pygame.K_DOWN,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(UP == True):
            op = self.Move.move(pygame.K_UP,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]
        if(LEFT == True):
            op = self.Move.move(pygame.K_LEFT,self.Prox)    
            self.x -= op[0]
            self.y -= op[1]

        self.x = max(0,self.x)
        self.y = max(0,self.y)

        self.x = min(self.X-20 -self.Player_size,self.x)
        self.y = min(self.Y-20 -self.Player_size,self.y)

        self.center_x = self.x+len(self.name)*2+self.Player_size/2
        self.center_y = self.y+20+self.Player_size/2

        if(SPACE == True) and self.state == 'Move' :
            if self.Prox.boom_num < self.Prox.max_boom_num :
                self.state = 'Boom'
                self.Prox.boom_num += 1
                curBoom = Boom.Boom(self.center_x,self.center_y,self)
                self.Attack(curBoom)

        if self.state == 'Boom' and (SPACE == False):
            self.state = 'Move'
        print(key,self.x,self.y)

    def DrawPlayer(self,screen):

        if self.show_name:
            tex = pygame.font.SysFont('宋体',size = 25)
            tex_fmt = tex.render(self.name+self.bias,1,'white')
            screen.blit(tex_fmt,(self.x,self.y))

        mycolcor = (255, 0, 0)
        position = ( self.x+len(self.name+self.bias)*2, self.y+20, self.Player_size, self.Player_size )
        
        width = 1
        pygame.draw.rect( screen, mycolcor, position, width )

        # print(self.center_x,self.center_y)

    def Attack(self,boom):
        config.get_global_BoomQueue().recive(boom)
