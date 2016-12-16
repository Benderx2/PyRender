import math
import numpy as np

def length(vec3):
	return math.sqrt(vec3[0]*vec3[0] + vec3[1]*vec3[1] + vec3[2]*vec3[2])

def length2(vec2):
	return math.sqrt(vec2[0]*vec2[0] + vec2[1] * vec2[1])

def normalize(vec3):
	vlength = length(vec3)
	v3 = [0.0,0,0]
	if(vlength != 0):
		inv = 1 / vlength
		return[vec3[0] * inv, vec3[1] * inv, vec3[2] * inv]
	return vec3
 
def trans_coordinate(coord, transmat):
	vec4 = [0.0,0.0,0,0]
	vec4[0] = coord[0] * transmat.item((0,0)) + (coord[1] * transmat.item((1,0))) + (coord[2] * transmat.item((2,0))) +  transmat.item((3,0))
	vec4[1] = coord[0] * transmat.item((0,1)) + (coord[1] * transmat.item((1,1))) + (coord[2] * transmat.item((2,1))) +  transmat.item((3,1))
	vec4[2] = coord[0] * transmat.item((0,2)) + (coord[1] * transmat.item((1,2))) + (coord[2] * transmat.item((2,2))) +  transmat.item((3,2))
	vec4[3] = 1.0 / (coord[0] * transmat.item((0,3)) + (coord[1] * transmat.item((1,3))) + (coord[2] * transmat.item((2,3))) +  transmat.item((3,3)))
	return [vec4[0]*vec4[3], vec4[1]*vec4[3], vec4[2]*vec4[3]]


def project(coord, transmat, width, height):
	pt = trans_coordinate(coord, transmat)
	x = pt[0] * width + width / 2.0
	y = -pt[1] * height + height / 2.0
	return [x,y]

def lookAtLH(eye, target, up):
	xaxis = [0.0,0,0]
	yaxis = [0.0,0,0]
	zaxis = [0.0,0,0]
	zaxis = np.subtract(target, eye)
	zaxis = normalize(zaxis)
	xaxis = np.cross(up, zaxis)
	xaxis = normalize(xaxis)
	yaxis = np.cross(zaxis, xaxis)
	mat = np.matrix([[1.0, 0, 0, 0],
					[0, 1.0, 0, 0],
					[0, 0, 1.0, 0],
					[0, 0, 0, 1.0]])

	mat.itemset((0,0), xaxis[0])
	mat.itemset((1,0), xaxis[1])
	mat.itemset((2,0), xaxis[2])

	mat.itemset((0,1), yaxis[0])
	mat.itemset((1,1), yaxis[1])
	mat.itemset((2,1), yaxis[2])

	mat.itemset((0,2), zaxis[0])
	mat.itemset((1,2), zaxis[0])
	mat.itemset((2,2), zaxis[0])

	mat.itemset((3,0), -np.dot(xaxis, eye))
	mat.itemset((3,1), -np.dot(yaxis, eye))
	mat.itemset((3,2), -np.dot(zaxis, eye))

	return mat

def perspectiveRH(fov, aspect, znear, zfar):
	yscale = 1 / (math.tan(fov*0.5))
	q = zfar / (znear - zfar)
	result = np.matrix( [[0.0,0,0,0],
						[0,0.0,0,0],
						[0,0,0.0,0],
						[0,0,0,0.0]])
	result.itemset((0,0), yscale/aspect)
	result.itemset((1,1), yscale)
	result.itemset((2,2), q)
	result.itemset((2,3), -1.0)
	result.itemset((3,2), q*znear)

	return result

def rotYawPitchRoll(yaw, pitch, roll):
	
	halfyaw = yaw*0.5
	halfpitch = pitch*0.5
	halfroll = roll*0.5

	sinyaw = math.sin(halfyaw)
	cosyaw = math.cos(halfyaw)
	sinpitch = math.sin(halfpitch)
	cospitch = math.cos(halfpitch)
	sinroll = math.sin(halfroll)
	cosroll = math.cos(halfroll)

	vec4 = [0.0,0.0,0.0,0.0]
	vec4[0] = (cosyaw * sinpitch * cosroll) + (sinyaw * cospitch * sinroll)
	vec4[1] = (sinyaw * cospitch * cosroll) - (cosyaw * sinpitch * sinroll)
	vec4[2] = (cosyaw * cospitch * sinroll) - (sinyaw * sinpitch * cosroll)
	vec4[3] = (cosyaw * cospitch * cosroll) + (sinyaw * sinpitch * sinroll)

	return vec4

def rotvec4tomat(vec4):
	xx = vec4[0]*vec4[0]
	yy = vec4[1]*vec4[1]
	zz = vec4[2]*vec4[2]
	xy = vec4[0]*vec4[1]
	zw = vec4[2]*vec4[3]
	zx = vec4[2]*vec4[0]
	yw = vec4[1]*vec4[3]
	yz = vec4[1]*vec4[2]
	xw = vec4[0]*vec4[3]
	result = np.matrix( [[1.0,0,0,0],
						[0,1.0,0,0],
						[0,0,1.0,0],
						[0,0,0,1.0]])
	
	result.itemset((0,0), 1.0 - (2.0 * (yy + zz)))
	result.itemset((0,1), 2.0 * (xy + zw))
	result.itemset((0,2), 2.0 * (zx - yw))
	result.itemset((1,0), 2.0 * (xy - zw))
	result.itemset((1,1), 1.0 - (2.0  * (zz + xx)))
	result.itemset((1,2), 2.0 * (yz + xw))
	result.itemset((2,0), 2.0 * (zx + yw))
	result.itemset((2,1), 2.0 * (yz - xw))
	result.itemset((2,2), 1.0 - (2.0 * (yy + xx)))

	return result

def rotmatrix(yaw, pitch, roll):
	return rotvec4tomat(rotYawPitchRoll(yaw, pitch, roll))

def translation(x, y, z):
	result = np.matrix( [[1.0,0,0,0],
						[0,1.0,0,0],
						[0,0,1.0,0],
						[0,0,0,1.0]])
	result.itemset((3,0), x)
	result.itemset((3,1), y)
	result.itemset((3,2), z)
	return result