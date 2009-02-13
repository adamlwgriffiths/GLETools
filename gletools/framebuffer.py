# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from __future__ import with_statement

from ctypes import byref
from pyglet.gl import *

from contextlib import nested

from .util import Context

__all__ = ['Framebuffer']

class Framebuffer(Context):
    _get = GL_FRAMEBUFFER_BINDING
    
    def bind(self, id):
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, id)

    def __init__(self):
        Context.__init__(self) 
        self._texture = None
        self._depth = None
        id = self.id = GLuint()
        glGenFramebuffersEXT(1, byref(id))
        
    def get_depth(self):
        return self._depth
    def set_depth(self, depth):
        self._depth = depth
        with self:
            glFramebufferRenderbufferEXT(
                GL_FRAMEBUFFER_EXT,
                GL_DEPTH_ATTACHMENT_EXT,
                GL_RENDERBUFFER_EXT,
                depth.id,
            )
    depth = property(get_depth, set_depth)

    def get_texture(self):
        return self._texture
    def set_texture(self, texture):
        self._texture = texture
        with nested(self, texture):
            glFramebufferTexture2DEXT(
                GL_FRAMEBUFFER_EXT,
                GL_COLOR_ATTACHMENT0_EXT,
                texture.target,
                texture.id,
                0,
            )
    texture = property(get_texture, set_texture)

