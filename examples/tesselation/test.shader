#version 400

vertex:
    in vec4 position;
    out vec4 color;

    uniform mat4 projection;
    uniform mat4 modelview;

    void main(void){
        gl_Position = projection * modelview * position;
    }

fragment:
    in vec4 color;
    out vec4 fragment;

    void main(){
        fragment = vec4(1.0, 0.0, 0.0, 0.5);
    }
