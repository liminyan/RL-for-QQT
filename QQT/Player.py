import numpy as np
import pygame,sys,time
import Boom
import config
import view


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
        self.speed = 4.5
        self.power = 2
        self.state = '0'
        self.boom_num = 0
        self.max_boom_num = 8


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
        self.center_y = self.y+self.Player_size/2+Player_size/2
        self.state = 'Move'
        self.bias = ''
        self.X = X
        self.Y = Y
        self.view = view.View(X,Y,Player_size)
        self.BoomView = np.zeros((int(X/Player_size),int(Y/Player_size)))
        self.view_size = 5


    def get_cur_state(self):

        view_size = self.view_size
        total_view = np.ones((2,view_size,view_size))
        state_view = total_view[0]
        total_view[1] *= 5
        Boom_view = total_view[1]


        std_x,std_y= int(self.center_x/self.Player_size),int(self.center_y/self.Player_size)
        shape = self.view.map.shape

        len_size = int((view_size-1)/2)

        view_x = 0
        view_y = 0

        tmpx = std_x - len_size
        tmpy = std_y - len_size
        begin_x = max(0,tmpx)
        begin_y = max(0,tmpy)

        if tmpx < 0:
            view_x -= tmpx

        if tmpy < 0:
            view_y -= tmpy

        end_x = min(shape[0]-1,std_x + len_size)
        end_y = min(shape[1]-1,std_y + len_size)
        len_x_size  = end_x - begin_x + 1
        len_y_size  = end_y - begin_y + 1
        state_view[view_x:view_x+len_x_size,view_y:view_y+len_y_size] = self.view.map[begin_x:begin_x+len_x_size,begin_y:begin_y+len_y_size]
        Boom_view[view_x:view_x+len_x_size,view_y:view_y+len_y_size] = self.BoomView[begin_x:begin_x+len_x_size,begin_y:begin_y+len_y_size]

        print(Boom_view.T)
        return total_view

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


    def move(self):

        if self.state == "Dead" :
            self.bias ='[Dead]'


        x = self.x
        y = self.y
        op_rank = 0
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_UP] == True):
            op = self.Move.move(pygame.K_UP,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 1

        elif(keys[pygame.K_DOWN] == True):
            op = self.Move.move(pygame.K_DOWN,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 2
        elif(keys[pygame.K_LEFT] == True):
            op = self.Move.move(pygame.K_LEFT,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 3
        elif(keys[pygame.K_RIGHT] == True):
            op = self.Move.move(pygame.K_RIGHT,self.Prox)    
            x -= op[0]
            y -= op[1]
            op_rank = 4
        if(keys[pygame.K_RETURN] == True):
            tex = pygame.font.SysFont('宋体',size = 25)
            tex_fmt = tex.render('[!]',1,'white')
            config.get_screen().blit(tex_fmt,(x + self.Player_size/2,y - self.Player_size/2))

        x = max(0.5*self.Player_size,x)
        y = max(0.5*self.Player_size,y)
        x = min(self.X -2.5*self.Player_size ,x)
        y = min(self.Y -2.5*self.Player_size,y)
        center_x = self.x+len(self.name)*2+self.Player_size/2
        center_y = self.y+self.Player_size/2+self.Player_size/2
        have_boom,std_x,std_y = self.view.fix(center_x,center_y)


        if op_rank and not self.check_corss(center_x,center_y,op_rank):
            self.center_x = std_x
            self.center_y = std_y
            self.x = x
            self.y = y


        if(keys[pygame.K_SPACE] == True) and self.state == 'Move' :
            if self.Prox.boom_num < self.Prox.max_boom_num :
                if not have_boom:
                    self.state = 'Boom'
                    self.Prox.boom_num += 1
                    curBoom = Boom.Boom(std_x,std_y,self)
                    self.Attack(curBoom)

        if self.state == 'Boom' and (keys[pygame.K_SPACE] == False):
            self.state = 'Move'

    def DrawPlayer(self,screen):

        self.get_cur_state()
        if self.show_name:
            tex = pygame.font.SysFont('宋体',size = 25)
            tex_fmt = tex.render(self.name+self.bias,1,'white')
            screen.blit(tex_fmt,(self.x,self.y))
        mycolcor = (0, 0, 255)
        mycolcor2 = (255, 255, 255)

        rate = 0.25
        position = ( self.x+len(self.name+self.bias)*2, self.y+self.Player_size/2, self.Player_size, self.Player_size )
        position2 = ( self.x+len(self.name+self.bias)*2+0.5*(1-rate)*self.Player_size, self.y+self.Player_size/2 + 0.5*(1-rate)*self.Player_size, self.Player_size*rate, self.Player_size*rate )
        
        width = 1
        pygame.draw.rect( screen, mycolcor, position, width )
        pygame.draw.rect( screen, mycolcor2, position2, width )


    def Attack(self,boom):
        config.get_global_BoomQueue().recive(boom)


