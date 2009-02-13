from __future__ import with_statement

import random
from contextlib import nested

import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, Texture, Framebuffer, projection, ortho, Sampler2D

window = pyglet.window.Window(fullscreen=True)
texture = Texture(window.width, window.height, format=GL_LUMINANCE, filter=GL_NEAREST)
framebuffer = Framebuffer()
framebuffer.texture = texture
program = ShaderProgram(
    FragmentShader.open('game_of_life.frag'),
)
program.vars.width = float(texture.width)
program.vars.height = float(texture.height)
program.vars.texture = Sampler2D(GL_TEXTURE0)

def quad():
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(window.width, window.height, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(window.width, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0.0, window.height, 0.0)
    glEnd()

def spawn_glider(delta):
    texture.retrieve()

    xoff = random.randint(3, texture.width-3)
    yoff = random.randint(3, texture.height-3)
    direction = random.randint(0, 3)
    
    if direction == 0:
        texture[xoff+1, yoff+0] = 255
        texture[xoff+2, yoff+1] = 255
        texture[xoff+0, yoff+2] = 255
        texture[xoff+1, yoff+2] = 255
        texture[xoff+2, yoff+2] = 255
    elif direction == 1:
        texture[xoff+1, yoff+2] = 255
        texture[xoff+2, yoff+1] = 255
        texture[xoff+0, yoff+0] = 255
        texture[xoff+1, yoff+0] = 255
        texture[xoff+2, yoff+0] = 255
    elif direction == 2:
        texture[xoff+1, yoff+0] = 255
        texture[xoff+0, yoff+1] = 255
        texture[xoff+2, yoff+2] = 255
        texture[xoff+1, yoff+2] = 255
        texture[xoff+0, yoff+2] = 255
    elif direction == 3:
        texture[xoff+1, yoff+2] = 255
        texture[xoff+0, yoff+1] = 255
        texture[xoff+2, yoff+0] = 255
        texture[xoff+1, yoff+0] = 255
        texture[xoff+0, yoff+0] = 255
        
    texture.update()

pyglet.clock.schedule(lambda delta:None)
pyglet.clock.schedule_interval(spawn_glider, 0.001)
fps = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    window.clear()
    with nested(framebuffer, program):
        glActiveTexture(GL_TEXTURE0)
        with texture:
            quad()
   
    with texture:
        quad()
    fps.draw()

if __name__ == '__main__':
    #spawn_glider(None)
    pyglet.app.run()
