from __future__ import with_statement

import sys
import re
import random
from contextlib import nested

import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, Texture, Framebuffer, projection, ortho, Sampler2D

class LifFormat(object):
    meta = re.compile(r'#(Life|D)')
    rule = re.compile(r'#([NR])')
    pattern = re.compile(r'#P (-?\d+) (-?\d+)')
    matchers = meta, rule, pattern
   
    @classmethod
    def match(cls, line):
        for matcher in cls.matchers:
            match = matcher.match(line)
            if match:
                return matcher, match.groups()
        return None, None

    @classmethod
    def parse_pattern(cls, lines):
        pattern = set()
        y = 0
        while lines and lines[0][0] != '#':
            line = lines.pop(0)
            x = 0
            for c in line:
                if c == '*':
                    pattern.add((x,y))
                x+=1
            y += 1
        return pattern

    @classmethod
    def parse(cls, filename):
        lines = [line.strip() for line in open(filename) if line.strip()]
        ruleset = None
        patterns = list()

        while lines:
            type, groups = cls.match(lines.pop(0))
            if type == cls.meta:
                pass
            elif type == cls.rule:
                ruleset = groups[0]
            elif type == cls.pattern:
                x, y = map(int, groups)
                pattern = cls.parse_pattern(lines)
                patterns.append((x,y,pattern))
        return ruleset, patterns

window = pyglet.window.Window(fullscreen=True)

framebuffer = Framebuffer()
front = Texture(window.width, window.height, format=GL_LUMINANCE, filter=GL_NEAREST)
back = Texture(window.width, window.height, format=GL_LUMINANCE, filter=GL_NEAREST)

program = ShaderProgram(
    FragmentShader.open('shader.frag'),
)
program.vars.width = float(front.width)
program.vars.height = float(front.height)
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

pyglet.clock.schedule(lambda delta:None)
fps = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    global front, back

    framebuffer.texture = front

    window.clear()
    with nested(framebuffer, program, back):
        quad()
   
    with front:
        quad()

    fps.draw()

    front, back = back, front

def spawn_random(x, y):
    xoff, yoff, pattern = random.choice(catalogue)
    xpos, ypos = x + xoff, y + yoff
    
    back.retrieve()
    for px, py in pattern:
        back[xpos+px, ypos+py] = 255
    back.update()

def spawn_whole(x, y):
    back.retrieve()
    for xoff, yoff, pattern in catalogue:
        xpos, ypos = x + xoff, y + yoff
        for px, py in pattern:
            back[xpos+px, ypos+py] = 255
    back.update()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        spawn_whole(x, y)
    else:
        spawn_random(x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        spawn_whole(x, y)
    else:
        spawn_random(x, y)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        ruleset, catalogue = LifFormat.parse(sys.argv[1])
    else:
        ruleset, catalogue = LifFormat.parse('patterns/gliders.lif')
    pyglet.app.run()
