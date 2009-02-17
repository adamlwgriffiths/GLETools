uniform float width, height;
uniform sampler2D texture;
uniform sampler2D depthmap;
varying float depth;

vec4 get(sampler2D texture, int x, int y){
    vec2 pos = vec2(gl_FragCoord.x, gl_FragCoord.y) + vec2(x, y); 
    return texture2D(texture, pos / vec2(width, height));
}

void main(){
    vec4 result = vec4(0.0, 0.0, 0.0, 0.0);
    float weight_sum = 0.0;
    for(int x=0; x<20; x++){
        for(int y=0; y<20; y++){
            vec4 color = get(texture, x-10, y-10);
            float sample_depth = get(depthmap, x-10, y-10).r;
            float factor = clamp(0.5 / (get(depthmap, 0, 0).r-depth), 0.5, 1.0);
            weight_sum += factor;
            result += color*factor;
        }
    }
    gl_FragColor = result/weight_sum + vec4(0.2, 0.2, 0.2, 0.0);
}
