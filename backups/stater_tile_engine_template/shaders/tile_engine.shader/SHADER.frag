#version 330

// Get all uniforms
uniform float TILE_SIZE;
uniform isampler2D tileMap;
uniform sampler2DArray tileAtlas;
uniform mat4 invView;

// Output
out vec4 fragCol;

// Main Function
void main() {
    // Calculate pixel coord
    vec2 worldSpaceFrag = (invView * vec4(gl_FragCoord.xy, 0.0, 1.0)).xy;
    vec2 gridTile = worldSpaceFrag/TILE_SIZE;
    vec2 uv = fract(gridTile);
    // Sampling
    ivec2 sample = ivec2(floor(gridTile));
    float tile = texelFetch(tileMap, sample, 0).r;
    fragCol = texture(tileAtlas, vec3(uv, tile));
}