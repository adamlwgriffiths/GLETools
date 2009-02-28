# -*- coding: utf-8 -*-
"""
    examples.ripples
    ~~~~~~~~~~~~~~~~

    :copyright: 2009 by Henri Tuhola <henri.tuhola@gmail.com> / Florian Boesch <pyalot@gmail.com>
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import with_statement
from contextlib import nested
import random

import pyglet
from gletools import (
    ShaderProgram, FragmentShader, Texture, Framebuffer, Sampler2D
)
from gletools.gl import *

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
        glColor4f(0.0, 1.5, 3.0, 1.0)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glVertex3f(x, y, 0)
        glVertex3f(x+rx, y+ry, 0)
        glEnd()

@window.event
def on_mouse_press(x, y, button, modifiers):
    with framebuffer:
        glColor4f(0.0, 1.5, 3.0, 1.0)
        glPointSize(4.0)
        glBegin(GL_POINTS)
        glVertex3f(x, y, 0)
        glEnd()

def rain(delta):
    x = random.randint(0, window.width)
    y = random.randint(0, window.height)
    size = random.random() * 3
    with framebuffer:
        glColor4f(0.0, size/2, size, 1.0)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex3f(x, y, 0)
        glEnd()

pyglet.clock.schedule_interval(rain, 0.2)
pyglet.clock.schedule(lambda delta: None)

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
        glColor4f(1.0, 1.0, 1.0, 1.0)
        quad(left=0, bottom=0, right=window.width, top=window.height)
    
    tex1, tex2, tex3 = tex2, tex3, tex1

if __name__=='__main__':
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    if gl_info.have_extension('ARB_color_buffer_float'):
        glClampColorARB(GL_CLAMP_VERTEX_COLOR_ARB, GL_FALSE)
        glClampColorARB(GL_CLAMP_FRAGMENT_COLOR_ARB, GL_FALSE)
        glClampColorARB(GL_CLAMP_READ_COLOR_ARB, GL_FALSE)
    pyglet.app.run()
