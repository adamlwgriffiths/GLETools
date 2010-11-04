#version 400

vertex:
    in vec4 position;

    uniform sampler2D terrain;
    
    void main(void){
        vec2 texcoord = position.xy;
        float height = texture(terrain, texcoord).a;
        vec4 displaced = vec4(position.x, position.y, height, 1.0);
        gl_Position = displaced;
    }

control:
    layout(vertices = 4) out;
    uniform vec2 screen_size;
    uniform mat4 projection;
    uniform mat4 modelview;
    
    bool offscreen(vec4 vertex){
        vec4 v = projection * vertex;
        v/=v.w;
        return any(
            lessThan(v.xy, vec2(-1.5)) ||
            greaterThan(v.xy, vec2(1.5))
        ) || vertex.z > 0.0;
    }

    void main(){
        if(gl_InvocationID == 0){
            vec4 v0 = (modelview * gl_in[0].gl_Position);
            vec4 v1 = (modelview * gl_in[1].gl_Position);
            vec4 v2 = (modelview * gl_in[2].gl_Position);
            vec4 v3 = (modelview * gl_in[3].gl_Position);
            if(all(bvec4(offscreen(v0), offscreen(v1), offscreen(v2), offscreen(v3)))){
                gl_TessLevelInner[0] = 0;
                gl_TessLevelInner[1] = 0;
                gl_TessLevelOuter[0] = 0;
                gl_TessLevelOuter[1] = 0;
                gl_TessLevelOuter[2] = 0;
                gl_TessLevelOuter[3] = 0;
            }
            else{
                float x = 5; 
                float e0 = round(clamp(x/length((v1.xyz+v2.xyz)/2), 1, 64));
                float e1 = round(clamp(x/length((v0.xyz+v1.xyz)/2), 1, 64));
                float e2 = round(clamp(x/length((v3.xyz+v0.xyz)/2), 1, 64));
                float e3 = round(clamp(x/length((v2.xyz+v3.xyz)/2), 1, 64));

                gl_TessLevelInner[0] = max(e1, e2);
                gl_TessLevelInner[1] = max(e0, e3);
                gl_TessLevelOuter[0] = e0;
                gl_TessLevelOuter[1] = e1;
                gl_TessLevelOuter[2] = e2;
                gl_TessLevelOuter[3] = e3;
            }
        }
        gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
    }

eval:
    layout(quads, equal_spacing, ccw) in;
    out vec2 texcoord;
    out float depth;

    uniform sampler2D terrain;
    uniform mat4 projection;
    uniform mat4 modelview;

    void main(){
        float u = gl_TessCoord.x;
        float v = gl_TessCoord.y;

        vec4 a = mix(gl_in[1].gl_Position, gl_in[0].gl_Position, u);
        vec4 b = mix(gl_in[2].gl_Position, gl_in[3].gl_Position, u);
        vec4 position = mix(a, b, v);
        texcoord = position.xy;
        float height = texture(terrain, texcoord).a;
        gl_Position = projection * modelview * vec4(texcoord, height, 1.0);
        depth = gl_Position.z*1.5;
    }

fragment:
    in vec2 texcoord;
    in float depth;
    out vec4 fragment;

    uniform sampler2D diffuse;
    uniform sampler2D terrain;

    vec3 incident = normalize(vec3(1.0, 0.2, 0.5));
    vec4 light = vec4(1.0, 0.95, 0.9, 1.0) * 1.1;

    void main(){
        vec3 normal = normalize(texture(terrain, texcoord).xyz);
        vec4 color = texture(diffuse, texcoord);

        float dot_surface_incident = max(0, dot(normal, incident));

        color = color * light * (max(0.1, dot_surface_incident)+0.05)*1.5;
        color = mix(color, color*0.5+vec4(0.5, 0.5, 0.52, 1.0), depth);

        fragment = color;
    }
