uniform float scale;
uniform vec2 offsets;
uniform sampler2D heightmap;

float get(float xoff, float yoff){
    vec2 pos = gl_TexCoord[0].st + (vec2(xoff, yoff)*offsets); 
    return texture2D(heightmap, pos).r * scale;
}

vec3 normal(float height, float xoff, float yoff){
    float _xoff = xoff * offsets.x;
    float _yoff = yoff * offsets.y;
    vec3 neighbor = vec3(_xoff, height-get(xoff, yoff), _yoff);
    return normalize(
        cross(neighbor, vec3(_yoff, 0.0, _xoff))
    );
}

void main(void){
    float height = get(0.0, 0.0);
    vec3 n = (
        normal(height,  1.0, -1.0) +
        normal(height,  1.0,  0.0) +
        normal(height,  1.0,  1.0) +
        normal(height,  0.0,  1.0) +
        normal(height,  0.0, -1.0) +
        normal(height, -1.0, -1.0) +
        normal(height, -1.0,  0.0) +
        normal(height, -1.0,  1.0)
    ) / 8.0;
    vec2 uv = gl_TexCoord[0].st;
    gl_FragData[0] = vec4(uv.s, height, uv.t, 1);
    gl_FragData[1].rgb = normalize(n)*0.5+0.5;
}
