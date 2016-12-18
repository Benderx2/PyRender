import pygame

global_screen = None
SCRN_HEIGHT = 480
SCRN_WIDTH = 640
global_font = None
clock = None

def initialise():
	global global_screen, global_font, clock
	pygame.init()
	global_screen = pygame.display.set_mode((SCRN_WIDTH, SCRN_HEIGHT))
	pygame.display.set_caption("PyRender Window")
	global_font = pygame.font.SysFont("./data/VeraMono.ttf", 30)
	clock = pygame.time.Clock()

def putpixel(x, y, r, g, b):
	global global_pixels, global_screen
	global_screen.fill((r, g, b),((x, y),(1,1)))
	
def text(string, x, y, r, g, b):
	global global_screen, global_font
	global_screen.blit(global_font.render(string, 1, (r,g,b)), (x, y))

def output_flush():
	pygame.display.flip()

def output_clear(r,g,b):
	global_screen.fill((r,g,b), ((0,0), (SCRN_WIDTH, SCRN_HEIGHT)))

def draw_point(pt):
	if pt[0] >= 0 and pt[1] >= 0 and int(pt[0]) < SCRN_WIDTH and int(pt[1]) < SCRN_HEIGHT:
		putpixel(int(pt[0]), int(pt[1]), 255, 255, 255)

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

def draw_triangle(A, B, C):
	global global_screen
	pygame.draw.polygon(global_screen, [0, 250, 0], [[int(A[0]), int(A[1])], [int(B[0]), int(B[1])], [int(C[0]), int(C[1])]], 1)