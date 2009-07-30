# -*- coding: utf-8 -*-
from __future__ import with_statement

import pyglet
from gletools import Framebuffer, Texture
from gletools.gl import *

window = pyglet.window.Window()
fbo = Framebuffer(
    Texture(window.width, window.height)
)

@window.event
def on_mouse_drag(x, y, rx, ry, button, modifier):
    if pyglet.window.mouse.LEFT == button:
        glColor4f(1,1,1,1)
        glLineWidth(3)
        with fbo:
            glBegin(GL_LINES)
            glVertex3f(x, y, 0)
            glVertex3f(x-rx, y-ry, 0)
            glEnd()

@window.event
def on_draw():
    window.clear()
    fbo.textures[0].draw()

if __name__ == '__main__':
    glEnable(GL_LINE_SMOOTH)
    pyglet.app.run()
