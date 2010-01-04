from __future__ import with_statement
from contextlib import nested

import pyglet
from gletools import (
    ShaderProgram, FragmentShader, VertexShader, Depthbuffer,
    Texture, Projection, Vec, Lighting, Color
)
from gletools.gl import *
from util import Mesh, Processor, Kernel, offsets, gl_init

### setup ###

window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height, near=18, far=50)
texture = Texture(window.width, window.height, GL_RGBA32F)
processor = Processor(texture)
bunny = Mesh('meshes/bunny')

### Application code ###

angle = 0.0
def simulate(delta):
    global angle
    angle += 10.0 * delta
pyglet.clock.schedule_interval(simulate, 0.01)

off = (1.0/window.width)*1.2, (1.0/window.height)*1.2
vertical = ShaderProgram(
    FragmentShader.open('shaders/gaussian/vertical.frag'),
    off = off,
)
horizontal = ShaderProgram(
    FragmentShader.open('shaders/gaussian/horizontal.frag'),
    off = off,
)

@window.event
def on_draw():
    window.clear()
    
    with nested(processor.renderto(texture), projection, Lighting, Color):
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glTranslatef(0, 0, -40)
        glRotatef(-65, 1, 0, 0)
        glRotatef(angle, 0.0, 0.0, 1.0)
        glRotatef(90, 1, 0, 0)
        glColor4f(0.5, 0.0, 0.0, 1.0)
        bunny.draw()
        glPopMatrix()

    for _ in range(5):
        processor.filter(texture, vertical)
        processor.filter(texture, horizontal)
    processor.blit(texture)

if __name__ == '__main__':
    gl_init()
    pyglet.app.run()
