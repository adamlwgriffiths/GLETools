# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import with_statement
from pyglet.gl import *
from ctypes import byref

_get_type_map = {
    int: (GLint, glGetIntegerv),
    float: (GLfloat, glGetFloatv),
}

def get(enum, size=1, type=int):
    type, accessor = _get_type_map[type]
    values = (type*size)()
    accessor(enum, values)
    if size == 1:
        return values[0]
    else:
        return values[:]

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

class MatrixMode(object):
    def __init__(self, mode):
        self.mode = mode

    def __enter__(self):
        glPushAttrib(GL_TRANSFORM_BIT)
        glMatrixMode(self.mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        glPopAttrib()

class Projection(object):
    def __init__(self, x, y, width, height, fov=55, near=0.1, far=100.0):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.fov = fov
        self.near, self.far = near, far

    def __enter__(self):
        glPushAttrib(GL_VIEWPORT_BIT)
        glViewport(self.x, self.y, self.width, self.height)
       
        with MatrixMode(GL_PROJECTION):
            glPushMatrix()
            glLoadIdentity()
            gluPerspective(self.fov, self.width / float(self.height), self.near, self.far)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with MatrixMode(GL_PROJECTION):
            glPopMatrix()

        glPopAttrib()

class Ortho(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def __enter__(self):
        glPushAttrib(GL_VIEWPORT_BIT)
        glViewport(self.x, self.y, self.width, self.height)

        with MatrixMode(GL_PROJECTION):
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(self.x, self.width, self.y, self.height)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        with MatrixMode(GL_PROJECTION):
            glPopMatrix()

        glPopAttrib()
