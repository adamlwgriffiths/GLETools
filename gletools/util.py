# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from ctypes import byref

def get(enum):
    value = GLint()
    glGetIntegerv(enum, byref(value))
    return value.value

class Context(object):
    def __init__(self):
        self.stack = list()

    def __enter__(self):
        self._enter()
        self.stack.append(get(self._get))
        self.bind(self.id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.check()
        id = self.stack.pop(-1)
        self.bind(id)
        self._exit()

    def _enter(self):
        pass

    def _exit(self):
        pass

    def check(self):
        pass
    
def projection(fov, width, height, near=0.1, far=100.0):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, width / float(height), near, far)
    glMatrixMode(GL_MODELVIEW)

def ortho(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0 * width, 0.0, 1.0 * height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
