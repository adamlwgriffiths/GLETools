const int max_kernel_size = 25;

uniform sampler2D texture;
uniform int kernel_size;
uniform vec2 offsets[max_kernel_size];
uniform float kernel[max_kernel_size];

void main(){
    int i;
    vec4 sum=vec4(0.0);
    for(i=0; i<kernel_size; i++){
        vec4 value = texture2D(texture, gl_TexCoord[0].st + offsets[i]);
        sum += value * kernel[i];
    }
    gl_FragColor = sum;
}
