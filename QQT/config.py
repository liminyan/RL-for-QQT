
def init():
	global global_BoomQueue
	global_BoomQueue = None

	global global_player
	global_player = None

	global boom_color
	boom_color = None

	global bar_color
	bar_color = None

	global screen
	screen = None

def set_global_BoomQueue(BoomQueue):
	global global_BoomQueue
	global_BoomQueue = BoomQueue

def set_global_player(player):
	global global_player
	global_player = player

def get_global_BoomQueue():
	return global_BoomQueue

def get_global_player():
	return  global_player

def set_boom_color(color):
	global boom_color
	boom_color = color

def set_bar_color(color):
	global bar_color
	bar_color = color

def set_screen( scr):
	global screen
	screen =  scr

def get_boom_color():
	return  boom_color

def get_bar_color():
	return  bar_color

def get_screen ():
	return  screen
