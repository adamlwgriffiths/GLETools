from __future__ import with_statement

import pyglet
from util import Mesh, gl_init, ChangeValue, nested, quad
from gletools.gl import *
from gletools import (
    Screen, Projection, Lighting, Color, VertexObject, Texture, Framebuffer,
    ShaderProgram, FragmentShader,
)

window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height, near=0.1, far=100)
angle = ChangeValue()
heightmap = Texture.open('images/heightmap.png')
width, height = heightmap.width, heightmap.height
texview = Screen(0, 0, width, height)

vertex_texture = Texture(width, height, GL_RGB)
normal_texture = Texture(width, height, GL_RGB)
fbo = Framebuffer(
    vertex_texture,
    normal_texture,
)
fbo.drawto = GL_COLOR_ATTACHMENT0_EXT, GL_COLOR_ATTACHMENT1_EXT
heightmap_normal = ShaderProgram(
    FragmentShader.open('shaders/heightmap_normal.frag'),
    offsets = (1.0/width, 1.0/height),
    scale = 0.2,
)

v3f = []
for z in range(height):
    for x in range(width):
        v3f.extend((x/float(width), 0, z/float(height)))

n3f = []
for z in range(height):
    for x in range(width):
        n3f.extend((0, 1, 0))

def index(x, y):
    return x+y*width

indices = []
for z in range(height-1):
    for x in range(width-1):
        indices.extend((
            index(x, z), index(x, z+1), index(x+1, z+1)        
        ))
        indices.extend((
            index(x, z), index(x+1, z+1), index(x+1, z)        
        ))

vbo = VertexObject(
    pbo                 = True,
    indices             = indices,
    dynamic_draw_v3f    = v3f,
    dynamic_draw_n3f    = n3f,
)
 
@window.event
def on_draw():
    window.clear()

    with nested(fbo, texview, heightmap, heightmap_normal):
        quad(width, height, 0, 0)
        vbo.v3f.copy_from(vertex_texture)
        vbo.n3f.copy_from(normal_texture)

    with nested(projection, Lighting):
        glPushMatrix()
        glTranslatef(0, 0, -1)
        glRotatef(20, 1, 0, 0)
        glRotatef(angle, 0.0, 1.0, 0.0)
        glTranslatef(-0.5, 0, -0.5)
        vbo.draw(GL_TRIANGLES)
        glPopMatrix()

    heightmap.draw(10, 10)
    vertex_texture.draw(148, 10)
    normal_texture.draw(286, 10)

if __name__ == '__main__':
    gl_init()
    pyglet.app.run()
