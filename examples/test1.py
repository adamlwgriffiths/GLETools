from __future__ import with_statement
from contextlib import nested

import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, Texture, Framebuffer, projection, ortho

window = pyglet.window.Window()
texture = Texture(64, 64, filter=GL_LINEAR)
framebuffer = Framebuffer()
framebuffer.textures[0] = texture
program = ShaderProgram(
    FragmentShader('''
    uniform float size;
    void main(){
        vec4 vec = vec4(gl_FragCoord.x-size/2, gl_FragCoord.y-size/2, 0.0, 1.0) / size;
        gl_FragColor = (normalize(vec) + 1) / 2;
    }''')
)
program.vars.size = 64.0
rotation = 0.0

def quad(min=0.0, max=1.0):
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(max, max, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(max, min, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(min, min, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(min, max, 0.0)
    glEnd()

def simulate(delta, _):
    global rotation
    rotation += 40.0 * delta

pyglet.clock.schedule(simulate, 0.03)
    
@window.event
def on_draw():
    window.clear()
    with nested(framebuffer, program):
        ortho(texture.width, texture.height)
        quad(0.0, texture.width)
   
    with texture:
        projection(45, window.width, window.height)
        glTranslatef(0, 0, -3)
        glRotatef(-45, 1, 0, 0)
        glRotatef(rotation, 0.0, 0.0, 1.0)
        quad(-1, 1)

if __name__ == '__main__':
    pyglet.app.run()
