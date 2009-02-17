import pyglet
from pyglet.gl import *

extensions = [
    'GL_EXT_framebuffer_object',
]

for extension in extensions:
    if not gl_info.have_extension(extension):
        raise Exception('%s not present'%extension)

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

window = pyglet.window.Window()

#create texture
texture = GLuint()
glGenTextures(1, byref(texture))
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
data = (GLubyte * (window.width * window.height * 4))()
glTexImage2D(
    GL_TEXTURE_2D, 0, GL_RGBA,
    window.width, window.height,
    0,
    GL_RGBA, GL_UNSIGNED_BYTE,
    data,
)
glBindTexture(GL_TEXTURE_2D, 0)
    
errors = {
    GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT:'GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT',
    GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT:'GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT: no image is attached',
    GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT:'GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT: attached images dont have the same size',
    GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT:'GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT: the attached images dont have the same format',
    GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT:'GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT',
    GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT:'GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT',
    GL_FRAMEBUFFER_UNSUPPORTED_EXT:'GL_FRAMEBUFFER_UNSUPPORTED_EXT',
}

#create fbo
framebuffer = GLuint()
glGenFramebuffersEXT(1, byref(framebuffer))

#attach texture
glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, framebuffer)
#glBindTexture(GL_TEXTURE_2D, texture)
glFramebufferTexture2DEXT(
    GL_FRAMEBUFFER_EXT,
    GL_COLOR_ATTACHMENT0_EXT,
    GL_TEXTURE_2D,
    texture,
    0,
)

#check for errors
status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
if status != GL_FRAMEBUFFER_COMPLETE_EXT:
    desc = errors[status]
    raise Exception(desc)

#glBindTexture(GL_TEXTURE_2D, 0)
glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

@window.event
def on_draw():
    window.clear()

    #draw into the fbo
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, framebuffer)
    quad(10, 50, 50, 10)
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

    #blit texture to screen
    glPushAttrib(GL_ENABLE_BIT)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    quad(0, window.width, window.height, 0)
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopAttrib()
   
if __name__ == '__main__':
    pyglet.app.run()
