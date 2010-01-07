# -*- coding: utf-8 -*-
"""
    examples.ripples
    ~~~~~~~~~~~~~~~~

    :copyright: 2009 by Henri Tuhola <henri.tuhola@gmail.com> / Florian Boesch <pyalot@gmail.com>
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import with_statement
from util import quad, nested, ChangeValue, gl_init, Processor
import random

import pyglet
from gletools import (
    Sampler2D, Screen, Color, Projection, Lighting, Texture
)
from gletools.gl import *
from ripples import Ripples
from r2vb import Heightmap
from gaussian import Gaussian

if __name__ == '__main__':
    angle = ChangeValue()
    window = pyglet.window.Window(width=786, height=600)
    projection = Projection(0, 0, window.width, window.height, near=0.1, far=100)
    width, height = 128, 128
    ripples = Ripples(width, height)
    height_texture = Texture(width*2, height*2)
    processor = Processor(height_texture)
    gaussian = Gaussian(processor)
    heightmap = Heightmap(width*2, height*2, scale=0.2)

    def rain(delta):
        x = random.randint(0, ripples.width)
        y = random.randint(0, ripples.height)
        size = random.random() * 0.8
        with nested(ripples.framebuffer, Color):
            glBegin(GL_QUADS)
            glColor4f(size, size, size, 1.0)
            glVertex3f(x-size, y-size, 0)
            glVertex3f(x+size, y-size, 0)
            glVertex3f(x+size, y+size, 0)
            glVertex3f(x-size, y+size, 0)
            glEnd()
        
    pyglet.clock.schedule_interval(rain, 0.2)
    pyglet.clock.schedule(lambda delta: None)

    @window.event
    def on_draw():
        window.clear()
        ripples.step()
        processor.copy(ripples.result, height_texture)
        gaussian.filter(height_texture, 1)
        heightmap.update_from(height_texture)
        
        with nested(projection, Lighting, Color):
            glColor3f(7/256.0, 121/256.0, 208/256.0)
            glPushMatrix()
            glTranslatef(0, 0, -1)
            glRotatef(20, 1, 0, 0)
            #glRotatef(angle, 0.0, 1.0, 0.0)
            glTranslatef(-0.5, 0, -0.5)
            heightmap.draw()
            glPopMatrix()

        ripples.result.draw()
        heightmap.vertex_texture.draw(2*width, 0, scale=0.5)
        heightmap.normal_texture.draw(4*width, 0, scale=0.5)

    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    gl_init()
    if gl_info.have_extension('ARB_color_buffer_float'):
        glClampColorARB(GL_CLAMP_VERTEX_COLOR_ARB, GL_FALSE)
        glClampColorARB(GL_CLAMP_FRAGMENT_COLOR_ARB, GL_FALSE)
        glClampColorARB(GL_CLAMP_READ_COLOR_ARB, GL_FALSE)
    pyglet.app.run()
