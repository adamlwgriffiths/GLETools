# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from __future__ import with_statement

from pyglet.gl import *

from .util import Context

__all__ = ['Texture']

class Object(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Texture(Context):

    gl_byte = Object(
        obj = GLubyte,
        enum = GL_UNSIGNED_BYTE
    )
    gl_short = Object(
        obj = GLushort,
        enum = GL_UNSIGNED_SHORT
    )
    gl_float = Object(
        obj = GLfloat,
        enum = GL_FLOAT,
    )
    gl_half_float = Object(
        obj = GLfloat,
        enum = GL_FLOAT,
    )

    rgb = Object(
        enum = GL_RGB,
        count = 3,
    )
    rgba = Object(
        enum = GL_RGBA,
        count = 4,
    )
    luminance = Object(
        enum  = GL_LUMINANCE,
        count = 1,
    )
    alpha = Object(
        enum = GL_ALPHA,
        count = 1,
    )

    specs = {
        GL_RGB:Object(
            type = gl_byte,
            channels = rgb,
        ),
        GL_RGBA:Object(
            type = gl_byte,
            channels = rgba,
        ),
        GL_RGB16:Object(
            type = gl_short,
            channels = rgb,
        ),
        GL_RGBA32F:Object(
            type = gl_float,
            channels = rgba,
        ),
        GL_RGB16F:Object(
            type = gl_half_float,
            channels = rgb,
        ),
        GL_RGB32F:Object(
            type = gl_float,
            channels = rgb,
        ),
        GL_LUMINANCE32F_ARB:Object(
            type = gl_float,
            channels = luminance,
        ),
        GL_LUMINANCE:Object(
            type = gl_byte,
            channels = luminance,
        ),
        GL_ALPHA:Object(
            type = gl_byte,
            channels = alpha,
        )
    }

    target = GL_TEXTURE_2D
    
    _get = GL_TEXTURE_BINDING_2D

    def bind(self, id):
        glBindTexture(self.target, id)

    def _enter(self):
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(self.target)

    def _exit(self):
        glPopAttrib()

    def __init__(self, width, height, format=GL_RGBA, filter=GL_LINEAR):
        Context.__init__(self)
        self.width = width
        self.height = height
        self.format = format
        self.filter = filter
        spec = self.spec = self.specs[format]
        self.buffer_type = (spec.type.obj * (width * height * spec.channels.count))
        id = self.id = GLuint()

        glGenTextures(1, byref(id))
        self.buffer = self.buffer_type()
        self.update()
        #self.set_data(buffer)
        
    def _quad(self, scale):
        t = 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0
        x1 = 0.0
        y1 = 0.0
        z = 0.0
        x2 = self.width * scale
        y2 = self.height * scale
        return (GLfloat * 32)(
             t[0],  t[1],  t[2],  1.0,
             x1,    y1,    z,     1.0,
             t[3],  t[4],  t[5],  1.0,
             x2,    y1,    z,     1.0,
             t[6],  t[7],  t[8],  1.0,
             x2,    y2,    z,     1.0,
             t[9],  t[10], t[11], 1.0,
             x1,    y2,    z,     1.0,
        )

    def set_data(self, data):
        with self:
            glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, self.filter)
            glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, self.filter)
            glTexImage2D(
                self.target, 0, self.format,
                self.width, self.height,
                0,
                self.spec.channels.enum, self.spec.type.enum,
                data,
            )
            glFlush()

    def draw(self, x=0, y=0, z=0, scale=1.0):
        glPushMatrix()
        glTranslatef(x, y, z)
        with self:
            glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
            glInterleavedArrays(GL_T4F_V4F, 0, self._quad(scale))
            glDrawArrays(GL_QUADS, 0, 4)
            glPopClientAttrib()
        glPopAttrib()
        glPopMatrix()

    def get_data(self, buffer):
        with self:
            glPushClientAttrib(GL_CLIENT_PIXEL_STORE_BIT)
            glGetTexImage(
                self.target, 0, self.spec.channels.enum, self.spec.type.enum,
                buffer,
            )
            glPopClientAttrib()

    def update(self):
        self.set_data(self.buffer)

    def retrieve(self):
        self.get_data(self.buffer)

    def __getitem__(self, (x, y)):
        x, y = x%self.width, y%self.height

        channels = self.spec.channels.count
        pos = (x + y * self.width) * channels
        if channels == 1:
            return self.buffer[pos]
        else:
            end = pos + channels
            return self.buffer[pos:end]

    def __setitem__(self, (x, y), value):
        x, y = x%self.width, y%self.height

        channels = self.spec.channels.count
        pos = (x + y * self.width) * channels
        if channels == 1:
            self.buffer[pos] = value
        else:
            end = pos + channels
            self.buffer[pos:end] = value
