import pygame
import numpy as np
import math3d as m3d
import pygame.gfxdraw
import sys
from pygame.locals import *
SCRN_HEIGHT = 480
SCRN_WIDTH = 640
RENDER_WIREFRAME = 1
RENDER_FILL = 0
global_screen = None
global_font = None
clock = None
global_pixels = []
zbuf = []
render_mode = RENDER_WIREFRAME
scroll_up = False
scroll_down = False

def initialise():
	global global_screen, global_font, clock, global_pixels, zbuf
	pygame.init()
	global_screen = pygame.display.set_mode((SCRN_WIDTH, SCRN_HEIGHT) )
	#global_screen.set_alpha(None)
	global_font = pygame.font.SysFont("Arial", 10)
	pygame.display.set_caption("PyRender Window")
	global_pixels = np.zeros(shape=(SCRN_WIDTH, SCRN_HEIGHT))
	zbuf = np.zeros(shape=(SCRN_WIDTH, SCRN_HEIGHT))
	zbuf.fill(sys.float_info.max)
	clock = pygame.time.Clock()

def update():
	global scroll_up, scroll_down
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == MOUSEBUTTONDOWN:
			if(event.button == 4):
				scroll_up = True
				scroll_down = False
			elif(event.button == 5):
				scroll_up = False
				scroll_down = True

def text(string, x, y, r, g, b):
	global global_screen, global_font
	global_screen.blit(global_font.render(string, 0, (r,g,b)), (x, y))

def loadimage(string, r, g, b):
	im = pygame.image.load(string).convert()
	im.set_colorkey((r, g, b))
	return im
# NOTE: DO NOT CALL THIS FUNCTION BEFORE OUTPUT_FLUSH()!
def blit_surface(surf, x, y):
	global global_screen
	global_screen.blit(surf,(x,y))

def output_flush():
	pygame.display.flip()

def output_clear(r,g,b):
	global global_screen
	global_screen.fill((r,g,b), (0,0,SCRN_WIDTH, SCRN_HEIGHT))


def draw_triangle(A, B, C, r, g, b):
	#draw_efficient_triangle([A, B, C], r, g, b)
	#pygame.draw.polygon(global_screen, [r,g,b], [[A[0], A[1]],[B[0], B[1]],[C[0], C[1]]], render_mode);
	pygame.gfxdraw.aapolygon(global_screen, [[A[0], A[1]],[B[0], B[1]],[C[0], C[1]]], [r,g,b]);
# FRONT END INPUT FUNCTIONS (MOUSE)
def mouse_getXY():
	return pygame.mouse.get_pos()

def mouse_relXY():
	return pygame.mouse.get_rel()

# Returns a tuple with the following booleans:
# (T/F, T/F, T/F)
# 	L 	M 	R
def mouse_getpress():
	#pygame.event.get()
	return pygame.mouse.get_pressed()

# Get Scroll direction, +1 if forward, 0 if no movement, -1 if movement backward
# This function resets the scroll mouse
def get_mousescroll():
	global scroll_up, scroll_down
	res = 0
	if(scroll_up == True):
		res = 1
	elif(scroll_down == True):
		res = -1
	scroll_up = False
	scroll_down = False
	return res