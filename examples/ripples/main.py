# -*- coding: utf-8 -*-
"""
    examples.ripples
    ~~~~~~~~~~~~~~~~

    :copyright: 2009 by Henri Tuhola <henri.tuhola@gmail.com> / Florian Boesch <pyalot@gmail.com>
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
tex1 = Texture(window.width, window.height, filter=GL_LINEAR, format=GL_RGBA32F)
tex2 = Texture(window.width, window.height, filter=GL_LINEAR, format=GL_RGBA32F)
tex3 = Texture(window.width, window.height, filter=GL_LINEAR, format=GL_RGBA32F)

program = ShaderProgram(
    FragmentShader.open('ripples.frag'),
)
program.vars.resolution = float(window.width), float(window.height)
program.vars.tex2 = Sampler2D(GL_TEXTURE1)
program.vars.tex3 = Sampler2D(GL_TEXTURE2)

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
        glColor4f(0.0, 0.7, 1.0, 1.0)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glVertex3f(x, y, 0)
        glVertex3f(x+rx, y+ry, 0)
        glEnd()

@window.event
def on_mouse_press(x, y, button, modifiers):
    with framebuffer:
        glColor4f(0.0, 0.7, 1.0, 1.0)
        quad(x-5, x+5, y+5, y-5)

def simulate(delta):
    pass

pyglet.clock.schedule(simulate)

@window.event
def on_draw():
    global tex1, tex2, tex3
    window.clear()
    framebuffer.textures[0] = tex1
    tex1.unit = GL_TEXTURE0
    tex2.unit = GL_TEXTURE1
    tex3.unit = GL_TEXTURE2

    with nested(framebuffer, program, tex2, tex3):
        quad(left=0, bottom=0, right=window.width, top=window.height)
    with tex1:
        quad(left=0, bottom=0, right=window.width, top=window.height)
    
    tex1, tex2, tex3 = tex2, tex3, tex1

if __name__=='__main__':
    pyglet.app.run()
