uniform vec2 resolution;
uniform sampler2D dest;
uniform sampler2D source;

vec4 get(sampler2D texture, int x, int y){
    vec2 pos = vec2(gl_FragCoord.x, gl_FragCoord.y) + vec2(x, y); 
    return texture2D(texture, pos / resolution);
}

void main(void){
    gl_FragColor = (get(source, -1,  0)
                  + get(source,  1,  0)
                  + get(source,  0,  1)
                  + get(source,  0, -1)) / 2.0 - get(dest, 0,0);
    gl_FragColor *= 0.999;
}
