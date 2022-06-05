import pygame,sys,time
from pygame.locals import *

class Env(object):
	"""docstring for Env"""
	def __init__(self, global_player,global_BoomQueue,screen):
		super(Env, self).__init__()
		self.global_player = global_player
		self.global_BoomQueue = global_BoomQueue
		self.screen = screen

	def generate_view(self,Player_size,X,Y):

		for event in pygame.event.get():#获取事件
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		for x in range(0,X,Player_size):
			for y in range(0,Y,Player_size):
				pygame.draw.line(self.screen,'red',(x,0),(x,Y))
				pygame.draw.line(self.screen,'red',(0,y),(X,y))

		for player in self.global_player:
			player.view.update(self.global_BoomQueue,self.global_player)
			player.move()
			player.DrawPlayer(self.screen)

		self.global_BoomQueue.update()
		self.global_BoomQueue.viewupdate(self.global_player)
		self.global_BoomQueue.DrawBooml(self.screen)
		self.global_BoomQueue.check_player(self.screen)
		
		pygame.display.update()
		self.screen.fill('black')

	def reset(self):
		for boom in self.global_BoomQueue.Booml:
			boom.state = "Dead"
		self.global_BoomQueue.update()


		for player in self.global_player:
			player.state = 'Move'
			player.bias = ''

	def end(self):

		Dead_num = 0
		for player in self.global_player:
			if player.state == 'Dead':
				Dead_num += 1

		return Dead_num + 1 >= len(self.global_player)
		