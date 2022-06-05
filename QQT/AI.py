import numpy as np
import Player
import pygame,time
import random
import Boom
import config
import view
 
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
            self.x = random.randint(0,self.X- Player_size/2  -Player_size)
            self.y = random.randint(0,self.Y- Player_size/2  -Player_size)

        self.show_name = True
        self.Player_size = Player_size
        self.center_x = self.x+len(self.name)*2+Player_size/2
        self.center_y = self.y+ Player_size/2 +Player_size/2
        self.state = 'Move'
        self.bias = ''
        self.first = time.time()
        self.space = time.time()
        self.key = 0
        self.view = view.View(X,Y,Player_size)
        self.Reward = 0

    def check_corss(self,x,y,op_rank):
        # up down left right 1,2,3,4
        have_boom,std_x,std_y = self.view.fix(self.center_x,self.center_y)
        tr_x = x/self.Player_size 
        tr_y = y/self.Player_size 
        std_x /= self.Player_size
        std_y /= self.Player_size
        op = []
        op.append([std_x ,std_y - 1])
        op.append([std_x ,std_y + 1])
        op.append([std_x - 1,std_y])
        op.append([std_x + 1,std_y])
        extern = 0
        if op_rank == 1 or op_rank == 2:
            res = abs(op[op_rank-1][1] - tr_y)
            
            if tr_x - int(tr_x) < 0.25 :
                extern = self.view.map[int(std_x) - 1][int(op[op_rank - 1][1])] == 1
            elif tr_x - int(tr_x) > 0.75 :
                extern = self.view.map[int(std_x) + 1][int(op[op_rank - 1][1])] == 1
        else:
            if tr_y - int(tr_y) < 0.25 :
                extern =  self.view.map[int(op[op_rank - 1][0])][int(std_y) - 1] == 1
            elif tr_y - int(tr_y) > 0.75 :
                extern =  self.view.map[int(op[op_rank - 1][0])][int(std_y) + 1] == 1
            res = abs(op[op_rank-1][0] - tr_x)
        return res < 0.8 and (self.view.map[int(op[op_rank-1][0])][int(op[op_rank-1][1])] == 1 or extern)



    def get_cur_state(self):

        


    def get_rand_atcion(self):
        key = self.key
        if time.time() - self.first >=0.1:
            key = random.randint(0,5)
            self.first = time.time()
        STOP = True
        UP = False
        DOWN = False
        LEFT = False
        RIGHT = False
        SPACE = False
        if key == 0:
            STOP = True
        if key == 1:
            LEFT = True
        if key == 2:
            UP = True
        if key == 3:
            RIGHT = True
        if key == 4:
            DOWN = True
        self.key = key
        if time.time() - self.space >=0.4 or key == 5:
            key = random.randint(0,5)
            self.space = time.time() 
        if key ==  5:
            SPACE = True

        return STOP,UP,DOWN,LEFT,RIGHT,SPACE

    def move(self):

        if self.state == "Dead" :
            self.bias ='[Dead]'
            return
        x = self.x
        y = self.y

        STOP,UP,DOWN,LEFT,RIGHT,SPACE = self.get_rand_atcion()

        op_rank = 0
        if(UP == True):
            op = self.Move.move(pygame.K_UP,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 1
        
        elif(DOWN == True):
            op = self.Move.move(pygame.K_DOWN,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 2
      
        elif(LEFT == True):
            op = self.Move.move(pygame.K_LEFT,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 3

        elif(RIGHT == True):
            op = self.Move.move(pygame.K_RIGHT,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 4

        x = max(0.5*self.Player_size,x)
        y = max(0.5*self.Player_size,y)
        x = min(self.X -2.5*self.Player_size ,x)
        y = min(self.Y -2.5*self.Player_size,y)
        center_x = x+len(self.name)*2+self.Player_size/2
        center_y = y+self.Player_size/2+self.Player_size/2
        have_boom,std_x,std_y = self.view.fix(center_x,center_y)

        if op_rank and not self.check_corss(center_x,center_y,op_rank):
            self.center_x = std_x
            self.center_y = std_y
            self.x = x
            self.y = y

        if(SPACE == True) and self.state == 'Move' :
            if self.Prox.boom_num < self.Prox.max_boom_num :
                # have_boom,std_x,std_y = self.view.fix(self.center_x,self.center_y)
                if not have_boom:
                    self.state = 'Boom'
                    self.Prox.boom_num += 1
                    curBoom = Boom.Boom(std_x,std_y,self)
                    self.Attack(curBoom)

        if self.state == 'Boom' and (SPACE == False):
            self.state = 'Move'

    def DrawPlayer(self,screen):

        if self.show_name:
            tex = pygame.font.SysFont('宋体',size = 25)
            tex_fmt = tex.render(self.name+self.bias,1,'white')
            screen.blit(tex_fmt,(self.x,self.y))

        mycolcor = (255, 0, 0)
        position = ( self.x+len(self.name+self.bias)*2, self.y+ self.Player_size/2 , self.Player_size, self.Player_size )
        
        width = 1
        pygame.draw.rect( screen, mycolcor, position, width )

    def Attack(self,boom):
        config.get_global_BoomQueue().recive(boom)
