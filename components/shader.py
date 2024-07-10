from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import glDeleteProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

class Shader():
	
	# filename
	v_name = "vert.glsl"
	f_name = "frag.glsl"

	@staticmethod
	def gen(path):


		try:
			with open(path + Shader.v_name, "r") as file:
				v_src = file.read()

			with open(path + Shader.f_name, "r") as file:
				f_src = file.read()

			shader = compileProgram(
				compileShader(v_src, GL_VERTEX_SHADER),
				compileShader(f_src, GL_FRAGMENT_SHADER)
			)

			return shader
		
		except FileNotFoundError as err:
			print("\nProblem finding required files in /shader/ directory.")
			print("Check shader files exist and names match definition in Shader component.\n")
			raise err

	@staticmethod
	def del_program(program):
		glDeleteProgram(program)