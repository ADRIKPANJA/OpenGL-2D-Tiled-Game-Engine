#version 330

// In
in vec2 uv;

// Uniforms
uniform sampler2D tex;

// Out
out vec4 fragCol;

// Main function
void main() {
    fragCol = texture(tex, uv).rgba;
}