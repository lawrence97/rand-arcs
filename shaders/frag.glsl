#version 330 core

in vec3 fcol;

out vec4 col;

void main()
{
    col = vec4(fcol.x, fcol.y, fcol.z, 1.0);
}