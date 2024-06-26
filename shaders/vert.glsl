#version 330 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 col;

uniform mat4 view;
uniform mat4 proj;

out vec3 fcol;

void main()
{
	fcol = col;
    gl_Position = proj * view * vec4(pos.x, pos.y, pos.z, 1.0);
}