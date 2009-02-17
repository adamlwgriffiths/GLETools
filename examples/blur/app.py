from __future__ import with_statement
from contextlib import nested

import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, Texture, Framebuffer, Depthbuffer, projection, ortho, Sampler2D

window = pyglet.window.Window()

framebuffer = Framebuffer()
framebuffer.textures = [
    Texture(window.width, window.height, filter=GL_LINEAR),
    Texture(window.width, window.height, filter=GL_LINEAR),
]
framebuffer.depth = Depthbuffer(window.width, window.height)
framebuffer.drawto = GL_COLOR_ATTACHMENT0_EXT, GL_COLOR_ATTACHMENT1_EXT

program = ShaderProgram(
    FragmentShader.open('shader.frag'),
)
program.vars.width = float(window.width)
program.vars.height = float(window.height)
program.vars.texture = Sampler2D(GL_TEXTURE0)

rotation = 0.0

def quad(left, right, top, bottom):
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(right, top, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(right, bottom, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(left, bottom, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(left, top, 0.0)
    glEnd()

def blur_geom():
    glPushMatrix()    
    glRotatef(90, 1.0, 0.0, 0.0)
    quad(left=-0.5, right=0.5, top=1, bottom=-1)
    glPopMatrix()

def simulate(delta):
    global rotation
    rotation += 40.0 * delta

pyglet.clock.schedule_interval(simulate, 0.01)
    
@window.event
def on_draw():
    window.clear()

    projection(45, window.width, window.height)
    glLoadIdentity()
    glTranslatef(0, 0, -3)
    glRotatef(-45, 1, 0, 0)
    glRotatef(rotation, 0.0, 0.0, 1.0)

    framebuffer.drawto = GL_COLOR_ATTACHMENT0_EXT, GL_COLOR_ATTACHMENT1_EXT
    with framebuffer:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.0, 1.0, 0.0)
        quad(left=-1, right=1, top=1, bottom=-1)

    framebuffer.drawto = [GL_COLOR_ATTACHMENT1_EXT]
    with nested(framebuffer, program, framebuffer.textures[0]):
        glColor3f(1.0, 1.0, 1.0)
        blur_geom()

    with framebuffer.textures[1]:
        ortho(window.width, window.height)
        glLoadIdentity()
        glColor4f(1.0, 1.0, 1.0, 1.0)
        quad(left=0, right=window.width, top=window.height, bottom=0)

if __name__ == '__main__':
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()
