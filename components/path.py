import glm
from OpenGL.GL import *
import numpy

class Path():
	arcs = 10
	segments = 60	# num of segments per arc
	point_col = [1, 1, 1]
	control_col = [0.9, 0.5, 0.0]

	def __init__(self):

		fsize = glm.sizeof(glm.float32)
		self.points = []
		self.controls = []
		self.curve = []

		# start point at origin
		self.points.extend([0, 0, 0, *Path.point_col])
		self.controls.extend(numpy.random.uniform(low=-5, high=5, size=3))
		self.controls.extend(Path.control_col)

		for i in range(1, Path.arcs):
			# last points location
			current = [self.points[-6], self.points[-5], self.points[-4]]
			# new random points
			next = numpy.random.uniform(low=-5, high=5, size=3)
			next_control = numpy.random.uniform(low=-5, high=5, size=3)

			# gen segments for arc
			for j in range(0, Path.segments):
				vert = []
				
				t = (j) / (Path.segments - 1)

				p0 = [current[0], current[1], current[2]]
				p1 = [next_control[0], next_control[1], next_control[2]]
				p2 = [next[0], next[1], next[2]]

				l0 = [
					((1-t)*p0[0]) + (t*p1[0]),
					((1-t)*p0[1]) + (t*p1[1]),
					((1-t)*p0[2]) + (t*p1[2]),
				]

				l1 = [
					((1-t)*p1[0]) + (t*p2[0]),
					((1-t)*p1[1]) + (t*p2[1]),
					((1-t)*p1[2]) + (t*p2[2]),
				]

				# final segment point + colour
				vert = [
					((1-t)*l0[0] + (t*l1[0])),
					((1-t)*l0[1] + (t*l1[1])),
					((1-t)*l0[2] + (t*l1[2])),

					0.7,
					0.5,
					0.8
				]

				self.curve.extend(vert)

			# add point and contorl to list
			self.points.extend(next)
			self.points.extend(Path.point_col)
			self.controls.extend(next_control)
			self.controls.extend(Path.control_col)

		self.g_curve = glm.array(glm.float32, *self.curve)
		self.g_points = glm.array(glm.float32, *self.points)
		self.g_controls = glm.array(glm.float32, *self.controls)
		
		self.curve_vao, self.points_vao, self.controls_vao = glGenVertexArrays(3)
		self.curve_vbo, self.points_vbo, self.controls_vbo = glGenBuffers(3)

		Path.buffer(self.curve_vao, self.curve_vbo, self.g_curve)
		Path.buffer(self.points_vao, self.points_vbo, self.g_points)
		Path.buffer(self.controls_vao, self.controls_vbo, self.g_controls)


	@staticmethod
	def buffer(vao, vbo, data):
		fsize = glm.sizeof(glm.float32)

		glBindVertexArray(vao)
		glBindBuffer(GL_ARRAY_BUFFER, vbo)
		glBufferData(GL_ARRAY_BUFFER, glm.sizeof(data), data.ptr, GL_STATIC_DRAW)

		# attrib - location, size, type, normalise, stride, offset
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, fsize * 6, ctypes.c_void_p(0))
		
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, fsize * 6, ctypes.c_void_p(fsize * 3))

		glBindVertexArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, 0)


	def __del__(self):
		glDeleteVertexArrays(3, (self.curve_vao, self.points_vao, self.controls_vao))
		glDeleteBuffers(3, (self.curve_vbo, self.points_vbo, self.controls_vbo))