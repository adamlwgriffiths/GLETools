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
    uniform mat4 mvp;
    uniform float lod_factor;
    
    bool offscreen(vec4 vertex){
        if(vertex.z < -0.5){
            return true;
        }
        return any(
            lessThan(vertex.xy, vec2(-1.7)) ||
            greaterThan(vertex.xy, vec2(1.7))
        );
    }
    
    vec4 project(vec4 vertex){
        vec4 result = mvp * vertex;
        result /= result.w;
        return result;
    }

    vec2 screen_space(vec4 vertex){
        return (clamp(vertex.xy, -1.3, 1.3)+1) * (screen_size*0.5);
    }

    float level(vec2 v0, vec2 v1){
        return clamp(distance(v0, v1)/lod_factor, 1, 64);
    }

    void main(){
        if(gl_InvocationID == 0){
            vec4 v0 = project(gl_in[0].gl_Position);
            vec4 v1 = project(gl_in[1].gl_Position);
            vec4 v2 = project(gl_in[2].gl_Position);
            vec4 v3 = project(gl_in[3].gl_Position);

            if(all(bvec4(offscreen(v0), offscreen(v1), offscreen(v2), offscreen(v3)))){
                gl_TessLevelInner[0] = 0;
                gl_TessLevelInner[1] = 0;
                gl_TessLevelOuter[0] = 0;
                gl_TessLevelOuter[1] = 0;
                gl_TessLevelOuter[2] = 0;
                gl_TessLevelOuter[3] = 0;
            }
            else{
                vec2 ss0 = screen_space(v0);
                vec2 ss1 = screen_space(v1);
                vec2 ss2 = screen_space(v2);
                vec2 ss3 = screen_space(v3);

                float e0 = level(ss1, ss2);
                float e1 = level(ss0, ss1);
                float e2 = level(ss3, ss0);
                float e3 = level(ss2, ss3);

                gl_TessLevelInner[0] = mix(e1, e2, 0.5);
                gl_TessLevelInner[1] = mix(e0, e3, 0.5);
                gl_TessLevelOuter[0] = e0;
                gl_TessLevelOuter[1] = e1;
                gl_TessLevelOuter[2] = e2;
                gl_TessLevelOuter[3] = e3;
            }
        }
        gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
    }

eval:
    layout(quads, fractional_odd_spacing, ccw) in;
    out vec2 texcoord;
    out float depth;

    uniform sampler2D terrain;
    uniform mat4 mvp;

    void main(){
        float u = gl_TessCoord.x;
        float v = gl_TessCoord.y;

        vec4 a = mix(gl_in[1].gl_Position, gl_in[0].gl_Position, u);
        vec4 b = mix(gl_in[2].gl_Position, gl_in[3].gl_Position, u);
        vec4 position = mix(a, b, v);
        texcoord = position.xy;
        float height = texture(terrain, texcoord).a;
        gl_Position = mvp * vec4(texcoord, height, 1.0);
        depth = gl_Position.z;
    }

fragment:
    in vec2 texcoord;
    in float depth;
    out vec4 fragment;

    uniform sampler2D diffuse;
    uniform sampler2D terrain;
    uniform sampler2D noise_tile;

    vec3 incident = normalize(vec3(1.0, 0.2, 0.5));
    vec4 light = vec4(1.0, 0.95, 0.9, 1.0) * 1.1;

    void main(){
        vec3 normal = normalize(texture(terrain, texcoord).xyz);
        vec4 color = texture(diffuse, texcoord);
        float noise_factor = texture(noise_tile, texcoord*32).r+0.1;

        float dot_surface_incident = max(0, dot(normal, incident));

        color = color * light * noise_factor * (max(0.1, dot_surface_incident)+0.05)*1.5;
        fragment = mix(color, color*0.5+vec4(0.5, 0.5, 0.5, 1.0), depth*2.0);
    }
