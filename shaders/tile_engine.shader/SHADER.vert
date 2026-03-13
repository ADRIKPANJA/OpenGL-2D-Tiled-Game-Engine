#version 330

// In
in vec2 in_pos;

// Out
uniform mat4 p;

// Main Function
void main() {
    gl_Position = p * vec4(in_pos, 0, 1);
}