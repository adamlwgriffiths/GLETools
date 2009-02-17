# -*- coding: utf-8 -*-
"""
    examples.ripples
    ~~~~~~~~~~~~~~~~

    :copyright: 2008 by Henri Tuhola <henri.tuhola@gmail.com>
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import with_statement
from contextlib import nested

import pyglet
from pyglet.gl import *
from gletools import (
    ShaderProgram, FragmentShader, Texture, Framebuffer, Sampler2D
)

window = pyglet.window.Window(fullscreen=True)
framebuffer = Framebuffer()
framebuffer.textures = [
    Texture(window.width, window.height, filter=GL_LINEAR, format=GL_RGBA32F),
    Texture(window.width, window.height, filter=GL_LINEAR, format=GL_RGBA32F)
]

program = ShaderProgram(
    FragmentShader.open('ripples.frag'),
)
program.vars.resolution = float(window.width), float(window.height)
program.vars.dest = Sampler2D(GL_TEXTURE0)
program.vars.source = Sampler2D(GL_TEXTURE1)

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

@window.event
def on_mouse_motion(x,y,rx,ry):
    with framebuffer:
        glColor3f(0.0, 0.7, 1.0)
        glPointSize(3.0)
        glBegin(GL_POINTS)
        glVertex3f(x, y, 0)
        glEnd()

def simulate(delta):
    pass

pyglet.clock.schedule_interval(simulate, 1.0/85.0)

phase = 0
@window.event
def on_draw():
    global phase
    window.clear()
    framebuffer.drawto = [GL_COLOR_ATTACHMENT0_EXT + phase]
    framebuffer.textures[0].unit = GL_TEXTURE0 + phase
    framebuffer.textures[1].unit = GL_TEXTURE0 + (phase + 1) % 2
    with nested(framebuffer, program):
        with nested(framebuffer.textures[0], framebuffer.textures[1]):
            quad(left=0, bottom=0, right=window.width, top=window.height)
    with framebuffer.textures[phase]:
        quad(left=0, bottom=0, right=window.width, top=window.height)
    phase = (phase+1)%2

if __name__=='__main__':
    pyglet.app.run()
