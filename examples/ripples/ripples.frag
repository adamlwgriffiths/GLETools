uniform vec2 resolution;
uniform sampler2D tex2;
uniform sampler2D tex3;
vec2 step = vec2(1.0, 1.0)/resolution;

vec4 get(sampler2D texture, int x, int y){
    vec2 pos = gl_TexCoord[0].st + vec2(x, y) * step; 
    return texture2D(texture, pos);
}

void main(void){
    vec4 sample = (
        get(tex3, -1,  0) +
        get(tex3,  1,  0) + 
        get(tex3,  0,  1) + 
        get(tex3,  0, -1)
    );
    gl_FragColor = (sample / 2.0 - get(tex2, 0,0)) * 0.998;
}
