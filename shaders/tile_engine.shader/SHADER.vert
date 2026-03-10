#version 330

in vec2 in_pos;

uniform mat4 p;

void main() {
    gl_Position = p * vec4(in_pos, 0, 1);
}