import pygame

global_screen = None
SCRN_HEIGHT = 480
SCRN_WIDTH = 640

def initialise():
	global global_screen, global_pixels
	pygame.init()
	global_screen = pygame.display.set_mode((SCRN_WIDTH, SCRN_HEIGHT))

def putpixel(x, y, r, g, b):
	global global_pixels, global_screen
	global_screen.fill((r, g, b),((x, y),(1,1)))
	

def output_flush():
	pygame.display.flip()

def output_clear(r,g,b):
	global_screen.fill((r,g,b), ((0,0), (SCRN_WIDTH, SCRN_HEIGHT)))

def draw_point(pt):
	if pt[0] >= 0 and pt[1] >= 0 and int(pt[0]) < SCRN_WIDTH and int(pt[1]) < SCRN_HEIGHT:
		putpixel(int(pt[0]), int(pt[1]), 0, 150, 0)

def draw_line(x1, y1, x2, y2):
	# Find distance
	v1 = [x1, y1]
	v2 = [x2, y2]
	line_length = length2(np.subtract(v2, v1))
	if line_length < 2:
		return
	middlepoint = [(x2 + x1)/2, (y2 + y1)/2]
	draw_point(middlepoint)
	draw_line(x1, y1, middlepoint[0], middlepoint[1])
	draw_line(middlepoint[0], middlepoint[1], x2, y2)

def draw_efficient_line(x1, y1, x2, y2):
	# Bresenham Line Alg.
	dx = abs(x2 - x1)
	dy = abs(y2 - y1)
	inc_x = 1 if (x1 < x2) else (-1)
	inc_y = 1 if (y1 < y2) else (-1)
	err = dx - dy
	nx1 = x1
	ny1 = y1
	while(True):
		draw_point([nx1, ny1])
		if((nx1 == x2) and (ny1 == y2)): break
		err2 = err * 2
		if(err2 > -dy): 
			err -= dy
			nx1 += inc_x
		if(err2 < dx):
			err += dx
			ny1 += inc_y