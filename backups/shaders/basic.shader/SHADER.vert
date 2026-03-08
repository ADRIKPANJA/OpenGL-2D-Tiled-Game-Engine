#version 330

in vec2 in_pos;
in vec3 in_col;

uniform mat4 mvp;

out vec3 col;

void main() {
    gl_Position = mvp * vec4(in_pos, 0, 1);
    col = in_col;
}