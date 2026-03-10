#version 330

uniform isampler2D tileMap;
uniform mat4 invView;

out vec4 fragCol;

void main() {
    vec2 worldSpaceFrag = (invView * vec4(gl_FragCoord.xy, 0.0, 1.0)).xy;
    ivec2 gridTile = ivec2(floor(worldSpaceFrag/64.0));
    int tile = texelFetch(tileMap, gridTile, 0).r;
    vec4 tmp;
    if (tile == 1) {
        tmp = vec4(1.0);
    }
    else {
        tmp = vec4(0.0);
    }
    fragCol = tmp;
}