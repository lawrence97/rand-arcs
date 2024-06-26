import glm
from OpenGL.GL import *

class Axis():
	
	def __init__(self):

		fsize = glm.sizeof(glm.float32)

		# 3 pos, 3 cols each vertex
		self.grid = [
			-5,  0,  0,  0.6,  0,  0,		
             5,  0,  0,  0.6,  0,  0,
             0, -5,  0,  0,  0.6,  0, 
             0,  5,  0,  0,  0.6,  0, 
             0,  0, -5,  0,  0,  0.7, 
             0,  0,  5,	 0,  0,  0.7
		]
		
		self.verts = glm.array(glm.float32, *self.grid)
		self.n_verts = 6

		self.vao = glGenVertexArrays(1)
		self.vbo =  glGenBuffers(1)

		glBindVertexArray(self.vao)

		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, glm.sizeof(self.verts), self.verts.ptr, GL_STATIC_DRAW)

		# attrib - location, size, type, normalise, stride, offset 
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, fsize * 6, ctypes.c_void_p(0))	
		glEnableVertexAttribArray(0)

		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, fsize * 6, ctypes.c_void_p(fsize * 3))
		glEnableVertexAttribArray(1)

		glBindVertexArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, 0)

	def __del__(self):
		glDeleteVertexArrays(1, (self.vao,))
		glDeleteBuffers(1, (self.vbo,))
