import glm
import glfw
import glfw.GLFW
from OpenGL.GL import *
from math import floor

from components.shader import Shader
from components.axis import Axis 
from components.path import Path

WIDTH = 800;
HEIGHT = 800;
SHADER_LOC = "./shaders/"
CLEAR_COLOUR = (0.14, 0.14, 0.14)
VIEW_POSITION = glm.vec3(0.0, -0.6, -12.0)
VIEW_ROTATION = glm.vec3(25.0, -45.0, 0.0)
VIEW_SCALE = 0.9

# glfw init
if not glfw.init():
	print("Problem initialising glfw.")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

# window init
window = glfw.create_window(WIDTH, HEIGHT, "scene", None, None)

if not window:
	print("Problem creating window.")
	glfw.terminate()

# options
glfw.set_window_attrib(window, glfw.RESIZABLE, False)
glfw.make_context_current(window)
glfw.swap_interval(1)

glClearColor(*CLEAR_COLOUR, 1.0)
glViewport(0, 0, WIDTH, HEIGHT)

# shader init
shader = Shader.gen(SHADER_LOC)
glUseProgram(shader)


# input
def key_callback(window, key, scancode, action, mods):
	if key == glfw.GLFW.GLFW_KEY_ESCAPE and action == glfw.GLFW.GLFW_PRESS:
		glfw.set_window_should_close(window, 1)
		return

	if key == glfw.GLFW.GLFW_KEY_LEFT:
		VIEW_ROTATION[1] = VIEW_ROTATION[1] + 2

	if key == glfw.GLFW.GLFW_KEY_RIGHT:
		VIEW_ROTATION[1] = VIEW_ROTATION[1] - 2

	# update transform
	view = glm.mat4(1.0)
	view = glm.translate(view, VIEW_POSITION)
	view = glm.rotate(view, glm.radians(VIEW_ROTATION[0]), glm.vec3(1.0, 0.0, 0.0))
	view = glm.rotate(view, glm.radians(VIEW_ROTATION[1]), glm.vec3(0.0, 1.0, 0.0))
	view = glm.rotate(view, glm.radians(VIEW_ROTATION[2]), glm.vec3(0.0, 0.0, 1.0))
	view = glm.scale(view, glm.vec3(VIEW_SCALE))
	glUniformMatrix4fv(view_uni, 1, GL_FALSE, glm.value_ptr(view))

glfw.set_key_callback(window, key_callback)


# transform
view = glm.mat4(1.0)
view = glm.translate(view, VIEW_POSITION)
view = glm.rotate(view, glm.radians(VIEW_ROTATION[0]), glm.vec3(1.0, 0.0, 0.0))
view = glm.rotate(view, glm.radians(VIEW_ROTATION[1]), glm.vec3(0.0, 1.0, 0.0))
view = glm.rotate(view, glm.radians(VIEW_ROTATION[2]), glm.vec3(0.0, 0.0, 1.0))
view = glm.scale(view, glm.vec3(VIEW_SCALE))

proj = glm.perspective(glm.radians(70), 1, 0.1, 200)

# uniforms
view_uni = glGetUniformLocation(shader, "view")
glUniformMatrix4fv(view_uni, 1, GL_FALSE, glm.value_ptr(view))

proj_uni = glGetUniformLocation(shader, "proj")
glUniformMatrix4fv(proj_uni, 1, GL_FALSE, glm.value_ptr(proj))

# axis
axis = Axis()

# path
path = Path()
draw_index = 0;
count = path.segments * (path.arcs - 1)

# time
start = glfw.get_time()
elapsed = 0
multiplier = 100

# update
while glfw.window_should_close(window) != True:

	# draw curve over time
	elapsed = glfw.get_time() - start
	draw_index = min(floor(elapsed * multiplier), count)

	glfw.poll_events()

	glClear(GL_COLOR_BUFFER_BIT)

	# axis
	glBindVertexArray(axis.vao)
	glDrawArrays(GL_LINES, 0, axis.n_verts)

	# curve and points
	glBindVertexArray(path.curve_vao)
	glDrawArrays(GL_LINE_STRIP, 0, draw_index)
	
	glPointSize(5)
	glBindVertexArray(path.points_vao)
	glDrawArrays(GL_POINTS, 0, path.arcs)

	glPointSize(3)
	glBindVertexArray(path.controls_vao)
	glDrawArrays(GL_POINTS, 0, path.segments)
		
		
	glfw.swap_buffers(window)

# end
del axis
del path
Shader.del_program(shader)
glfw.destroy_window(window)
glfw.terminate