import numpy as np
import Boom


class View(object):
	"""docstring for View"""
	def __init__(self, X,Y,Player_size):
		super(View, self).__init__()
		# self.arg = arg

		print(X,Y,Player_size)
		self.Player_size = Player_size

		self.x = int(X/Player_size)
		self.y = int(Y/Player_size)
		self.map = np.zeros((self.x,self.y))
		self.Bdict = {}
		self.Pdict = {}



	def fix(self,ox,oy):
		std_x,std_y = int(ox/self.Player_size),int(oy/self.Player_size)
		have_boom = (self.map[std_x][std_y] == 1)
		return have_boom,std_x*self.Player_size + self.Player_size /2 ,std_y*self.Player_size+ self.Player_size /2
		# return 0,ox,oy

	def update(self,global_BoomQueue,global_player):
		self.map = (self.map+1)  * 0
		self.Bdict = {}
		self.Pdict = {}

		for bm in global_BoomQueue.Booml:
			ox,oy = bm.x,bm.y
			std_x,std_y = int(ox/self.Player_size),int(oy/self.Player_size)
			self.map[std_x][std_y] = 1
			key = str(std_x)+'_' +str(std_y)
			self.Bdict[key] = bm

		for pl in global_player:
			ox,oy = pl.center_x,pl.center_y
			std_x,std_y = int(ox/self.Player_size),int(oy/self.Player_size)
			self.map[std_x][std_y] = -1
			key = str(std_x)+'_' +str(std_y)
			self.Pdict[key] = pl

		# print(self.map.T)

