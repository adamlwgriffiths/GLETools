from __future__ import with_statement
from contextlib import nested

import pyglet
from gletools import ShaderProgram, FragmentShader, Texture, Framebuffer, Projection, Screen
from gletools.gl import *

from random import random
from util import quad, Processor
from gaussian import Gaussian

window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height)
noise = ShaderProgram(
    FragmentShader.open('shaders/noise.frag'),
    seed = 0.5,
)
width, height = 64, 64 
noise_texture = Texture(width, height, format=GL_RGBA32F)
Processor(noise_texture).filter(noise_texture, noise)
texture = Texture(64, 64, format=GL_RGBA32F)
processor = Processor(texture)
processor.copy(noise_texture, texture)
#processor.filter(texture, noise)
gaussian = Gaussian(processor)
gaussian.filter(texture, 2)

rotation = 0.0
def simulate(delta, _):
    global rotation
    rotation += 10.0 * delta
pyglet.clock.schedule(simulate, 0.03)
    
@window.event
def on_draw():
    window.clear()

    with nested(projection, texture):
        glPushMatrix()
        glTranslatef(0, 0, -3)
        glRotatef(-45, 1, 0, 0)
        glRotatef(rotation, 0.0, 0.0, 1.0)
        quad(-1, 1, 1, -1)
        glPopMatrix()

if __name__ == '__main__':
    pyglet.app.run()

