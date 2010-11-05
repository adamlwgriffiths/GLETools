from contextlib import nested
from ctypes import c_float, c_uint
import math

import pyglet
from pyglet.gl import *

from gletools import ShaderProgram, VertexObject, Matrix, Vector, Texture, Sampler2D, DepthTest

from util import View

def make_plane(width, height):
    v4f = (c_float*(width*height*4))()
    width_factor, height_factor = 1.0/float(width), 1.0/float(height)
    for y in xrange(height):
        for x in xrange(width):
            offset = (x+y*width)*4
            v4f[offset:offset+4] = x*width_factor, y*height_factor, -3, 1

    i_width, i_height = width-1, height-1
    indices = (c_uint*(i_width*i_height*4))()
    for y in xrange(i_height):
        for x in xrange(i_width):
            offset = (x+y*i_width)*4
            p1 = x+y*width
            p2 = p1+width
            p4 = p1+1
            p3 = p2+1
            indices[offset:offset+4] = p1, p2, p3, p4

    return VertexObject(
        indices = indices,
        v4f     = v4f,
    )

rotation = 0.0
zoom = 1.0
def simulate(delta, _):
    global rotation
    global rotation, zoom
    rotation += 0.02 * delta
    zoom = (math.sin(rotation*10)+1) * 0.5 + 0.2
    view.update(delta)

pyglet.clock.schedule(simulate, 0.03)

config = Config(buffers=2, samples=4)
window = pyglet.window.Window(config=config, fullscreen=True, vsync=False)
view = View(window)

diffuse = Texture.raw_open('data/mountains.diffuse', 2048, 2048, mipmap=4, format=GL_RGBA32F, filter=GL_LINEAR_MIPMAP_LINEAR, unit=GL_TEXTURE0, clamp='st')
terrain = Texture.raw_open('data/mountains.terrain', 2048, 2048, format=GL_RGBA32F, unit=GL_TEXTURE1, clamp='st')

program = ShaderProgram.open('terrain.shader',
    diffuse = Sampler2D(GL_TEXTURE0),
    terrain = Sampler2D(GL_TEXTURE1),
    lod_factor = 4.0,
)

test = ShaderProgram.open('test.shader',
    terrain = Sampler2D(GL_TEXTURE1),
)

vbo = make_plane(64, 64)
fps = pyglet.clock.ClockDisplay(color=(1,0,0,0.5))

@window.event
def on_draw():
    window.clear()

    model = Matrix().rotatex(-0.25).translate(-0.5, -0.5, 0.0)
    projection = Matrix.perspective(window.width, window.height, 60, 0.0001, 100.0)
    modelview = view.matrix * model

    program.vars.modelview = modelview
    program.vars.projection = projection
    program.vars.screen_size = float(window.width), float(window.height)

    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    with nested(DepthTest, diffuse, terrain, program):
        glPatchParameteri(GL_PATCH_VERTICES, 4);
        vbo.draw(GL_PATCHES)
    
    test.vars.modelview = modelview
    test.vars.projection = projection
   
    '''
    glDisable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    with nested(DepthTest, terrain, test):
        vbo.draw(GL_QUADS)
    '''
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    fps.draw()

if __name__ == '__main__':
    glCullFace(GL_BACK)
    glClearColor(1,1,1,1)
    pyglet.app.run()
