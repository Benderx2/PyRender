class obj_model(object):
	def __init__(self, model_name):
		self.vertices = []
		self.faces = []
		self.texcoords = []
		self.normals = []
		for line in open(model_name, "r"):
			if line == "":
				# EOF Encountered
				break
			if line.startswith('#'): continue
			values = line.split()
			if not values: continue
			if values[0] == 'v':
				# Vertex defined
				self.vertices.append([float(values[1]), float(values[2]), float(values[3])])
			elif values[0] == 'vn':
				self.normals.append([float(values[1]), float(values[2]), float(values[3])])
			elif values[0] == 'vt':
				self.texcoords.append([float(values[1]), float(values[2])])
			elif values[0] == 'f':
				face = []
				for v in values[1:]:
					w = v.split('/')
					face.append(int(w[0])-1)
				self.faces.append(face)
