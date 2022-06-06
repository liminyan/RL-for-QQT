import config,time
import pygame
import view
import numpy as np

class Boom(object):
    """docstring for Boom"""
    def __init__(self, x,y,player):
        super(Boom, self).__init__()
        self.x,self.y = x,y
        self.time = 5
        self.begin_time = None
        self.boom_begin_time = None
        self.state = 'Live'
        self.boom_time = 0.125
        self.player = player
        self.drawboom = False
        self.power = player.Prox.power

    def set_begin_time(self):
        self.begin_time = time.time()

    def get_state(self):
        end = time.time()

        if self.state == 'Boom':
            if end - self.boom_begin_time >= self.boom_time:
                self.state = 'Dead'
                return    self.state  
        if end - self.begin_time >= self.time:
            if self.state == 'Live':
                self.state = 'Boom'
                self.boom_begin_time = time.time()
                return     self.state

        return self.state

    def update(self):
        state = self.get_state()
        if state == 'Dead':
            self.player.Prox.boom_num -= 1

        return state


class BoomQueue(object):
    """docstring for BoomQueue"""
    def __init__(self,X,Y,Player_size):
        super(BoomQueue, self).__init__()
        self.Booml = []
        self.X = X
        self.Y = Y
        self.Player_size = Player_size
        self.view = view.View(X,Y,Player_size)
        self.Bdict = {}
        self.visit = {}
        self.BoomView = np.zeros((int(X/Player_size),int(Y/Player_size)))

    def get_boom_num(self):
        return len(self.Booml)

    def recive(self,boom):

        boom.set_begin_time()
        self.Booml.append(boom)

    def update(self):
        for boom in self.Booml:
            boom.update()
            if boom.state == 'Dead':
                self.Booml.remove(boom)

    def viewupdate(self,global_player):
        self.view.update(self,global_player)

        
    def DrawBoom(self,boom,screen):
        clolor = config.get_bar_color()
        position = boom.x , boom.y
        radius = self.Player_size /2
        width = 2
        pygame.draw.circle( screen, clolor, position, radius, width )
        tex = pygame.font.SysFont('宋体',size = 25)
        cur = time.time()
        begin = boom.begin_time 
        exist = boom.time
        rest_num = round(exist - (cur - begin),1)

        tex_fmt = tex.render(str(rest_num),1,'white')
        screen.blit(tex_fmt,(boom.x,boom.y))

    def DrawBoom_Boom(self,boom,screen):

        mycolcor =config.get_boom_color()
        center_x,center_y = boom.x , boom.y

        power = boom.power
        size = self.Player_size
        width = 0

        position = ( center_x-size/2, center_y-size/2, size*(power+1) , size )
        pygame.draw.rect( screen, mycolcor, position, width )
        position = ( center_x-size/2, center_y-size/2, size , size*(power+1) )
        pygame.draw.rect( screen, mycolcor, position, width )

        position = ( center_x-size/2 -power*size, center_y-size/2, power*size, size )
        pygame.draw.rect( screen, mycolcor, position, width )
        position = ( center_x-size/2 ,center_y-size/2 -power*size, size, power*size )
        pygame.draw.rect( screen, mycolcor, position, width )
      

    def expend_view(self,boom,exist = -1):
        if boom.state == "Dead":
            return

        power = boom.power
        shape = self.view.map.shape
        if exist == -1:
            cur = time.time()
            begin = boom.begin_time 
            exist = round((cur - begin),1)

        if boom.state == 'Boom':
            exist = boom.time
        # up
        cur_x,cur_y = int(boom.x/self.Player_size),int(boom.y/self.Player_size)
        self.BoomView[cur_x][cur_y] = max(self.BoomView[cur_x][cur_y],exist)
        for x in range(0,power):
            if cur_x - 1 >= 0:
                cur_x-=1
                key = str(cur_x)+'_' +str(cur_y)
                self.BoomView[cur_x][cur_y] = max(self.BoomView[cur_x][cur_y],exist)
                if key in self.Bdict and self.visit[self.Bdict[key]] == 0:
                    self.visit[self.Bdict[key]] = 1
                    self.expend_view(self.Bdict[key],exist = exist)
        # down
        cur_x,cur_y = int(boom.x/self.Player_size),int(boom.y/self.Player_size)
        for x in range(0,power):
            if cur_x + 1 < shape[0]:
                cur_x+=1
                key = str(cur_x)+'_' +str(cur_y)
                self.BoomView[cur_x][cur_y] = max(self.BoomView[cur_x][cur_y],exist)
                if key in self.Bdict and self.visit[self.Bdict[key]] == 0:
                    self.visit[self.Bdict[key]] = 1
                    self.expend_view(self.Bdict[key],exist = exist)
        # left
        cur_x,cur_y = int(boom.x/self.Player_size),int(boom.y/self.Player_size)
        for y in range(0,power):
            if cur_y - 1 >= 0:
                cur_y-=1
                key = str(cur_x)+'_' +str(cur_y)
                self.BoomView[cur_x][cur_y] = max(self.BoomView[cur_x][cur_y],exist)
                if key in self.Bdict and self.visit[self.Bdict[key]] == 0:
                    self.visit[self.Bdict[key]] = 1
                    self.expend_view(self.Bdict[key],exist = exist)
        # right
        cur_x,cur_y = int(boom.x/self.Player_size),int(boom.y/self.Player_size)
        for y in range(0,power):
            if cur_y + 1 < shape[1]:
                cur_y +=1
                key = str(cur_x)+'_' +str(cur_y)
                self.BoomView[cur_x][cur_y] = max(self.BoomView[cur_x][cur_y],exist)
                if key in self.Bdict and self.visit[self.Bdict[key]] == 0:
                    self.visit[self.Bdict[key]] = 1
                    self.expend_view(self.Bdict[key],exist = exist)
                    
    def boom_view(self):
        self.Bdict = {}
        for boom in self.Booml:
            self.visit[boom] = 0
            std_x,std_y = int(boom.x/self.Player_size),int(boom.y/self.Player_size)
            key = str(std_x)+'_' +str(std_y)
            self.Bdict[key] = boom

        for boom in self.Booml:
            if self.visit[boom] == 0:
                self.expend_view(boom,exist = -1)

    def clear_boom_view(self):
        self.BoomView *= 0

    def expend(self,boom):
        for _ in self.Booml:
            if _.state == 'Live':
                if _.x == boom.x:
                    if abs(_.y - boom.y) <= boom.power * self.Player_size:
                        _.state = 'Boom'
                        _.boom_begin_time = time.time()
                        self.expend(_)
                elif _.y == boom.y:
                    if abs(_.x - boom.x) <= boom.power * self.Player_size:
                        _.state = 'Boom'
                        _.boom_begin_time = time.time()
                        self.expend(_)

    def DrawBooml(self,screen):
        for boom in self.Booml:
            if boom.state == 'Boom':
                self.expend(boom)
        for boom in self.Booml:
            if boom.state == 'Live':
                self.DrawBoom(boom,screen)
            if boom.state == 'Boom':
                self.DrawBoom_Boom(boom,screen)  

    def check_player(self,screen):
        self.boom_view()
        for player in config.get_global_player():
            if player.state != 'Dead':
                cur_x,cur_y = int(player.center_x/self.Player_size),int(player.center_y/self.Player_size)
                if self.BoomView[cur_x][cur_y] == 5:
                	player.state = 'Dead'
            player.BoomView = self.BoomView.copy()
        self.clear_boom_view()


                

