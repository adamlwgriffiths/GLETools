from __future__ import with_statement
from contextlib import nested

import pyglet
from gletools import (
    ShaderProgram, FragmentShader, VertexShader, Depthbuffer,
    Texture, Framebuffer, Projection, Screen, Vec, Lighting
)
from gletools.gl import *

### pyglet/perspective setup ###

window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height, near=18, far=50)
screen = Screen(0, 0, window.width, window.height)

### Geometry ###

def quad(top, right, bottom, left):
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(bottom, right, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(bottom, left, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(top, left, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(top, right, 0.0)
    glEnd()

class Bunny(object):
    def __init__(self):
        v3f = [float(c)*0.2 for c in open('bunny/vertices').read().strip().split()]
        n3f = map(float, open('bunny/normals').read().strip().split())
        faces = map(int, open('bunny/faces').read().strip().split())
        self.display = pyglet.graphics.vertex_list_indexed(len(v3f)/3, faces,
            ('v3f', v3f),
            ('n3f', n3f),
        )

    def draw(self):
        self.display.draw(GL_TRIANGLES)

bunny = Bunny()

### Shaders and helpers ###

def offsets(min, max, window):
    result = []
    for x in range(min, max+1):
        for y in range(min, max+1):
            xoff = float(x)/float(window.width)
            yoff = float(y)/float(window.height)
            result.append(xoff)
            result.append(yoff)
    return Vec(2, result)

framebuffer = Framebuffer(
    Texture(window.width, window.height, GL_RGBA32F)
)
framebuffer.depth = Depthbuffer(window.width, window.height)

depth = ShaderProgram(
    VertexShader.open('shaders/normal.vert'),
    FragmentShader.open('shaders/depth.frag'),
)

laplace_orange_book = ShaderProgram(
    VertexShader.open('shaders/normal.vert'),
    FragmentShader.open('shaders/convolution.frag'),
    kernel_size = 3*3,
    kernel = Vec(1, [
        0,  1,  0,
        1, -4,  1,
        0,  1,  0,
    ]),
    offsets = offsets(-1, 1, window),
)

laplace = ShaderProgram(
    FragmentShader.open('shaders/convolution.frag'),
    kernel_size = 3*3,
    kernel = Vec(1, [
        -1, -1, -1,
        -1,  8, -1,
        -1, -1, -1,
    ]),
    offsets = offsets(-1, 1, window),
)

laplace_large = ShaderProgram(
    FragmentShader.open('shaders/convolution.frag'),
    kernel_size = 5*5,
    kernel = Vec(1, [
        -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1,
        -1, -1, 24, -1, -1,
        -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1,
    ]),
    offsets = offsets(-2, 2, window),
)

### Application code ###

#edge = laplace_orange_book
edge = laplace
#edge = laplace_large

angle = 0.0
def simulate(delta):
    global angle
    angle += 10.0 * delta
pyglet.clock.schedule_interval(simulate, 0.01)
    
@window.event
def on_draw():
    window.clear()
    
    with nested(framebuffer, projection, Lighting, depth):
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
    
    with nested(framebuffer.textures[0], screen, edge):
        glColor4f(1.0, 1.0, 1.0, 1.0)
        quad(window.width, window.height, 0, 0)

def gl_init():
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat*4)(0.1, 0.1, 0.1, 0.2))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat*4)(0.5, 0.5, 0.5, 0.8))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat*4)(0.3, 0.3, 0.3, 0.5))
    glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*4)(0, 30, 0, 1))

if __name__ == '__main__':
    gl_init()
    pyglet.app.run()

