#version 330

in vec2 in_pos;
in vec2 in_uv;

uniform mat4 mvp;

out vec2 uv;

void main() {
    gl_Position = mvp * vec4(in_pos, 0, 1);
    uv = in_uv;
}