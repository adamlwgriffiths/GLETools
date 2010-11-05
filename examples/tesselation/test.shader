#version 400

vertex:
    in vec4 position;
    uniform sampler2D terrain;
    uniform mat4 modelview;
    uniform mat4 projection;
    
    void main(void){
        vec2 texcoord = position.xy;
        float height = texture(terrain, texcoord).a;
        vec4 displaced = vec4(position.x, position.y, height, 1.0);
        gl_Position = projection * modelview * displaced;
    }

fragment:
    out vec4 fragment;
    void main(){
        fragment = vec4(1, 0, 0, 1);
    }
