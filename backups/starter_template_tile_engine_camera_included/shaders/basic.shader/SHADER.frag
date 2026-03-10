#version 330

in vec2 uv;

uniform sampler2D tex;

out vec4 fragCol;

void main() {
    fragCol = texture(tex, uv).rgba;
}