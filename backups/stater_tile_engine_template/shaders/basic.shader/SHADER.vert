#version 330

// In
in vec2 in_pos;
in vec2 in_uv;

// Uniforms
uniform mat4 mvp;

// Out
out vec2 uv;

// Main Function
void main() {
    gl_Position = mvp * vec4(in_pos, 0, 1);
    uv = in_uv;
}