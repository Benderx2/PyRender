import numpy as np
import math
import pygame
import random
import pyximport
pyximport.install()
import frontend as fnd
import math3d as m3d
import model as mdl

global_eventsq = []

class obj_camera(object):
	def __init__(self, pos, target):
		self.pos = [0,0,0]
		self.target = [0,0,0]
		self.pos = pos
		self.target = target

class obj_mesh(object):
	def __init__(self, v, pos, rot):
		self.vertices = []
		self.pos = [0,0,0]
		self.rot = [0,0,0]
		self.faces = []
		self.vertices = v
		self.pos = pos
		self.rot = rot
	def add_face(self, f):
		self.faces.append(f)

class obj_sprite(object):
	def __init__(self, image, x, y, w, h, c):
		self.w = 0
		self.h = 0
		self.image = fnd.loadimage(image, c[0], c[1], c[2])
		self.w = w
		self.h = h
		self.x = x
		self.y = y
		self.c = c
	def setpos(self, x, y):
		self.x = x
		self.y = y
	def load(self, imagepath, w, h, c):
		self.image = fnd.loadimage(imagepath, c[0], c[1], c[2])
		self.w = w
		self.h = h
		self.c = c
	def display(self):
		fnd.blit_surface(self.image, self.x, self.y)

class obj_event(object):
	def __init__(self, freq, func):
		self.frequency = 0
		self.function = 0
		self.ncount = 0
		self.frequency = freq
		self.function = func
		self.ncount = freq

def model_to_mesh(model, pos, rot):
	mesh = obj_mesh(model.vertices, pos, rot)
	for f in model.faces:
		mesh.add_face(f)
	return mesh

def render2d(sprites):
	for i in sprites:
		i.display()
	fnd.output_flush()

def sortTriangles(n):
	# average of Z-coordinates
	return -((n[0][2] + n[1][2] + n[2][2]) / 3)

def render3d(camera, meshes):
	fnd.output_clear(0,0,0)
	viewmat = m3d.lookAtLH(camera.pos, camera.target, [0,1.0,0])
	projmat = m3d.perspectiveRH(0.90, fnd.SCRN_WIDTH / fnd.SCRN_HEIGHT, 0.01, 1.0)
	cdef unsigned int i, j, poly
	triangles = []
	for i in range(0, len(meshes)):
		worldmat = m3d.rotmatrix(meshes[i].rot[1], meshes[i].rot[0], meshes[i].rot[2]) * m3d.translation(meshes[i].pos[0], meshes[i].pos[1], meshes[i].pos[2])
		transmat = worldmat * viewmat * projmat
		for j in range(0, len(meshes[i].faces)):
			ptA = m3d.project(meshes[i].vertices[meshes[i].faces[j][0]], transmat, fnd.SCRN_WIDTH, fnd.SCRN_HEIGHT)
			ptB = m3d.project(meshes[i].vertices[meshes[i].faces[j][1]], transmat, fnd.SCRN_WIDTH, fnd.SCRN_HEIGHT)
			ptC = m3d.project(meshes[i].vertices[meshes[i].faces[j][2]], transmat, fnd.SCRN_WIDTH, fnd.SCRN_HEIGHT)
			# Draw a triangle ABC
			color = (0.25 + (j % len(meshes[i].faces)) * 0.75/len(meshes[i].faces))*255
			triangles.append([ptA, ptB, ptC, color, color, color])
			poly += 1
	triangles.sort(key=sortTriangles)
	for t in triangles:
		fnd.draw_triangle(t[0], t[1], t[2], t[3], t[4], t[5])
	fnd.text(str(int(fnd.clock.get_fps())) + ' FPS', 0, 0, 255, 255, 30)
	fnd.text("Mouse X: " + str(fnd.mouse_getXY()[0]) + ", Mouse Y: " + str(fnd.mouse_getXY()[1]), 0, 10, 255, 0, 0);
	fnd.text("Polygons: " + str(poly), 0, 20, 0, 255, 0)
	fnd.output_flush()

def add_event(frequency, func):
	global global_eventsq
	# If interval is 0, it occurs every cycle
	# Interval is a measure of the no. of cycles 
	ev = obj_event(frequency, func)
	global_eventsq.append(ev)

def events(eventseq):
	if(len(eventseq) == 0): return

	for x in range(0, len(eventseq)):
		if(eventseq[x].ncount == 0):
			eventseq[x].function()
			eventseq[x].ncount = eventseq[x].frequency
		else:
			eventseq[x].ncount -= 1

def main_loop():
	global global_screen
	done = False
	sample_mesh = model_to_mesh(mdl.obj_model('./data/model.obj'), [0,0,0], [3,0,0])
	sample_sprite = obj_sprite("./data/pyrender.png", fnd.SCRN_WIDTH - 160, fnd.SCRN_HEIGHT - 48, 160, 48, (255, 255, 255))
	cam = obj_camera([0,0,15.0], [0,0,0])
	while True:
		fnd.update()
		render3d(cam, [sample_mesh])
		render2d([sample_sprite])
		L, M, R = fnd.mouse_getpress()
		if (M == True):
			move_x, move_y = fnd.mouse_relXY()
			sample_mesh.rot[1] -= (0.01 * move_x)
			sample_mesh.rot[0] += (0.01 * move_y)
		if(M == False):
			# Flush it
			fnd.mouse_relXY()
		addz = -(fnd.get_mousescroll() * 1.0) * abs(((cam.pos[2] * 1.0) / 50))
		cam.pos[2] += addz
		events(global_eventsq)
		fnd.clock.tick(60)

def engine_start():
	fnd.initialise()
	fnd.render_mode = fnd.RENDER_WIREFRAME
	main_loop()
