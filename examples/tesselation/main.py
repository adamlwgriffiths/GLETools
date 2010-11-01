import pyglet
from gletools import (
    ShaderProgram, TessControlShader, TessEvalShader, GeometryShader, VertexShader, FragmentShader,
    Texture, Framebuffer, Projection, VertexObject, Matrix
)

from gletools.gl import *

window = pyglet.window.Window()
rotation = 0.0

vbo = VertexObject(
    indices = [0, 1, 2, 0, 2, 3],
    v4f     = [
        +1, +1, 0, 1,
        +1, -1, 0, 1,
        -1, -1, 0, 1,
        -1, +1, 0, 1,
    ],
)

program = ShaderProgram.open('tesselation.shader',
    inner_level = 8.0,
    outer_level = 8.0,
)

#program = ShaderProgram.open('test.shader')

def simulate(delta, _):
    global rotation
    rotation += 0.1 * delta

pyglet.clock.schedule(simulate, 0.03)

@window.event
def on_draw():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    window.clear()

    program.vars.modelview = Matrix().rotatez(rotation).rotatex(-0.175).translate(0,0,-3)
    program.vars.projection = Matrix.perspective(window.width, window.height, 60, 0.1, 100.0)

    with program:
        vbo.draw(GL_PATCHES)
        #vbo.draw(GL_TRIANGLES)

if __name__ == '__main__':
    pyglet.app.run()
