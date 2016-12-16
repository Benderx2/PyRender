import numpy as np
import math
import pygame
import random
import math3d as m3d
import frontend as fnd

clock = pygame.time.Clock()

global_eventsq = []


class obj_camera(object):
	pos = [0,0,0]
	target = [0,0,0]
	def __init__(self, pos, target):
		self.pos = pos
		self.target = target


class obj_mesh(object):
	vertices = []
	pos = [0,0,0]
	rot = [0,0,0]
	faces = []
	def __init__(self, v, pos, rot):
		self.vertices = v
		self.pos = pos
		self.rot = rot
	def add_face(self, f):
		self.faces.append(f)

class obj_event(object):
	frequency = 0
	function = 0
	ncount = 0
	def __init__(self, freq, func):
		self.frequency = freq
		self.function = func
		self.ncount = freq

def render3d(camera, meshes):
	fnd.output_clear(0,0,0)
	viewmat = m3d.lookAtLH(camera.pos, camera.target, [0,1.0,0])
	projmat = m3d.perspectiveRH(0.78, fnd.SCRN_WIDTH / fnd.SCRN_HEIGHT, 0.01, 1.0)
	for i in range(0, len(meshes)):
		worldmat = m3d.rotmatrix(meshes[i].rot[1], meshes[i].rot[0], meshes[i].rot[2]) * m3d.translation(meshes[i].pos[0], meshes[i].pos[1], meshes[i].pos[2])
		transmat = worldmat * viewmat * projmat
		for j in range(0, len(meshes[i].faces)):
			ptA = m3d.project(meshes[i].vertices[meshes[i].faces[j][0]], transmat, fnd.SCRN_WIDTH, fnd.SCRN_HEIGHT)
			ptB = m3d.project(meshes[i].vertices[meshes[i].faces[j][1]], transmat, fnd.SCRN_WIDTH, fnd.SCRN_HEIGHT)
			ptC = m3d.project(meshes[i].vertices[meshes[i].faces[j][2]], transmat, fnd.SCRN_WIDTH, fnd.SCRN_HEIGHT)
			# Draw a triangle ABC
			fnd.draw_efficient_line(int(ptA[0]), int(ptA[1]), int(ptB[0]), int(ptB[1]))
			fnd.draw_efficient_line(int(ptB[0]), int(ptB[1]), int(ptC[0]), int(ptC[1]))
			fnd.draw_efficient_line(int(ptC[0]), int(ptC[1]), int(ptA[0]), int(ptA[1]))

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
	sample_mesh = obj_mesh([[-1,1,1], 
							[1,1,1],
							[-1,-1,1],
							[1,-1,1],
							[-1,1,-1],
							[1,1,-1],
							[1,-1,-1],
							[-1,-1,-1]], [0,0,0], [0,0,0])
	
	sample_mesh.add_face([0,1,2])
	sample_mesh.add_face([1,2,3])
	sample_mesh.add_face([1,3,6])
	sample_mesh.add_face([1,5,6])
	sample_mesh.add_face([0,1,4])
	sample_mesh.add_face([1,4,5])
	sample_mesh.add_face([2,3,7])
	sample_mesh.add_face([3,6,7])
	sample_mesh.add_face([0,2,7])
	sample_mesh.add_face([0,4,7])
	sample_mesh.add_face([4,5,6])
	sample_mesh.add_face([4,6,7])

	cam = obj_camera([0,0,10.0], [0,0,0])
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		render3d(cam, [sample_mesh])
		sample_mesh.rot[0] += 0.01
		sample_mesh.rot[1] += 0.01
		events(global_eventsq)
		clock.tick(60)

fnd.initialise()
main_loop()