import config,time
import pygame
class Boom(object):
    """docstring for Boom"""
    def __init__(self, x,y,player):
        super(Boom, self).__init__()
        self.x,self.y = x,y
        self.time = 5
        self.begin_time = None
        self.boom_begin_time = None
        self.state = 'Live'
        self.boom_time = 1.5
        self.player = player
        self.drawboom = False

    def set_begin_time(self):
        self.begin_time = time.time()

    def get_state(self):
        end = time.time()

        if self.state == 'Boom':
            if end - self.begin_time >= self.boom_time:
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

    def recive(self,boom):

        boom.set_begin_time()
        self.Booml.append(boom)
        print(len(self.Booml),boom.player.state)

    def update(self):
        for boom in self.Booml:
            boom.update()
            if boom.state == 'Dead':
                self.Booml.remove(boom)
        
    def DrawBoom(self,boom,screen):
        clolor = config.get_bar_color()
        position = boom.x , boom.y
        radius = self.Player_size /2
        width = 2
        pygame.draw.circle( screen, clolor, position, radius, width )

    def DrawBoom_Boom(self,boom,screen):

        mycolcor =config.get_boom_color()
        center_x,center_y = boom.x , boom.y

        power = boom.player.Prox.power
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
      

    def check_boom (self,center_x,center_y,screen):
        size = self.Player_size
        left,up = max(int(center_x-size/2),0) ,max(int(center_y-size/2),0)
        right,down = int(center_x+size/2) ,int(center_y+size/2)

        for x in range(left,right,5):
            for y in range(up,down,5):
                if screen.get_at((x,y)) == config.get_boom_color():
                    return 'Dead'

        return 'Live'



    def DrawBooml(self,screen):
        for _ in self.Booml:
            for boom in self.Booml:
                if boom.state == 'Live':
                    if self.check_boom(boom.x , boom.y,screen) == "Dead":
                    	boom.state = 'Boom'
                    if boom.state == 'Boom':
                        boom.boom_begin_time = time.time()

                if boom.state == 'Live':
                    self.DrawBoom(boom,screen)

                if boom.state == 'Boom' and boom.drawboom == False:
                    boom.drawboom == True
                    self.DrawBoom_Boom(boom,screen)                

    def check_player(self,screen):
        for player in config.get_global_player():
            if player.state != 'Dead':
                cur = self.check_boom(player.center_x , player.center_y,screen)
                if cur == 'Dead':
                	player.state = cur
                

