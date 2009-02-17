uniform float width, height;
uniform sampler2D texture;

vec4 get(int x, int y){
    vec2 pos = vec2(gl_FragCoord.x, gl_FragCoord.y) + vec2(x, y); 
    return texture2D(texture, pos / vec2(width, height));
}

void main(){
    vec4 result = vec4(0.0, 0.0, 0.0, 0.0);
    for(int x=0; x<20; x++){
        for(int y=0; y<20; y++){
            result += get(x-10, y-10);
        }
    }
    gl_FragColor = result/(20*20)/2 + vec4(0.5, 0.5, 0.5, 0.0);
}
