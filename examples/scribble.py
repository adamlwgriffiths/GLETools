# -*- coding: utf-8 -*-
from __future__ import with_statement
from contextlib import nested

import pyglet
from gletools import Framebuffer, Texture
from gletools.gl import *

window = pyglet.window.Window()
texture = Texture(window.width, window.height)
framebuffer = Framebuffer()
framebuffer.textures[0] = texture

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
def on_mouse_drag(x, y, rx, ry, button, modifier):
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    if pyglet.window.mouse.LEFT == button:
        glColor4f(1,1,1,1)
        glPointSize(3)
        glLineWidth(3)
    else:
        glColor4f(0,0,0,0)
        glPointSize(24)
        glLineWidth(24)
    with nested(framebuffer):
        glBegin(GL_LINES)
        glVertex3f(x, y, 0)
        glVertex3f(x-rx, y-ry, 0)
        glEnd()
        glBegin(GL_POINTS)
        glVertex3f(x, y, 0)
        glVertex3f(x-rx, y-ry, 0)
        glEnd()
    glDisable(GL_POINT_SMOOTH)
    glDisable(GL_LINE_SMOOTH)

@window.event
def on_draw():
    window.clear()
    glColor4f(1,1,1,1)
    with texture:
        quad(left=0, right=texture.width, top=texture.height, bottom=0)

if __name__=='__main__':
    pyglet.app.run()
