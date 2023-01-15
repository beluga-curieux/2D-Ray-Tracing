import numpy as np
# import maraudersMap as backend

import pygame as pg

'''réorganisation'''



class DataDisplay:
	def __init__(self, data={}, mod='top_right',color=(255, 255, 255),bgcolor=(0, 0, 0),size=20):
		# self.surf = pg.surface.Surface()
		self.mod =  mod # bottom_left bottom_right top_left top_right
		self.data = data
		self.size = size
		self.color = color
		self.bgcolor = bgcolor

	def update_data(self,dict: dict):
		self.data.update(dict)


	def draw(self,surface=None):
		self.font_object = pg.font.Font('textures/SmallMemory.ttf', self.size)
		self.string = "".join([f"  {cey}: {value}  " for cey, value in self.data.items()])
		self.data_surf = self.font_object.render(self.string, True, self.color)
		bg_surf = pg.surface.Surface(self.data_surf.get_size())
		bg_surf.fill(self.bgcolor)
		bg_surf.blit(self.data_surf,(0,0))

		if self.mod == 'top_right':
			surface.blit(bg_surf, (surface.get_size()[0]-(bg_surf.get_size()[0]), 5))
		elif self.mod == 'top_left':
			surface.blit(bg_surf, (0, 5))
		elif self.mod == 'bottom_left':
			surface.blit(bg_surf, (0, surface.get_size()[1]-bg_surf.get_size()[1]))
		elif self.mod == 'bottom_right':
			surface.blit(bg_surf, (surface.get_size()[0]-(self.size+5), 5))

if __name__ == '__main__':
	pg.init()
	color1 = (255, 255, 255)
	color2 = (0, 0, 0)
	pg_win = Win(color2, color1)
	clock = pg.time.Clock()

	pg_win.set_array_pos(-1,4)

	while True:
		clock.tick(60)

		if pg.event.get(pg.QUIT):
			# print("\n", co.Fore.RED + "END", sep='', end='')
			break
		pg.display.update()
		pg_win.aparecium(np.array([[1,0,1],[1,1,1],[0,0,1]]))


