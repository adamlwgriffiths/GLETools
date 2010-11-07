from ctypes import c_float, c_uint

from pyglet.window import key
from pyglet.input.evdev import get_devices
from pyglet.clock import schedule

from gletools import Matrix, Vector, VertexObject

class Navigator(object):
    def __init__(self):
        for device in get_devices():
            if device.name == '3Dconnexion SpaceNavigator':
                break
        self.device = device
        device.open()
        self.axes = {
            'x' : self.get('x'),
            'y' : self.get('y'),
            'z' : self.get('z'),
            'rx' : self.get('rx'),
            'ry' : self.get('ry'),
            'rz' : self.get('rz'),
        }

    def get(self, name):
        for control in self.device.controls:
            if control.name == name:
                return control

    def __getattr__(self, name):
        value = self.axes[name].value/255.0 
        if value > 0.0:
            return value*value
        else:
            return -value*value

class View(object):
    def __init__(self, window):
        self.rotation = Vector()
        self.rotspeed = Vector()
        self.position = Vector(0, 0, -1)
        self.speed = Vector()
        self.keys = key.KeyStateHandler()
        self.navigator = Navigator()
        schedule(self.update)

    def update(self, delta):
        delta = min(delta, 0.03)
        rotmatrix = Matrix().rotatex(self.rotation.y).rotatey(self.rotation.x)
        front =  rotmatrix * Vector(0.0, 0.0, 1.0, 1.0)
        right =  rotmatrix * Vector(1.0, 0.0, 0.0, 1.0)
        up =  rotmatrix * Vector(0.0, 1.0, 0.0, 1.0)

        factor = 0.5 * delta

        self.speed += right * -self.navigator.x * factor * 0.5
        self.speed += up * self.navigator.z * factor * 0.5
        self.speed += front * -self.navigator.y * factor * 0.5
        self.rotspeed += Vector(self.navigator.rz * factor, -self.navigator.rx * factor)

        self.rotspeed -= self.rotspeed * 1.0 * delta
        self.speed -= self.speed * 1.0 * delta

        self.rotation += self.rotspeed * delta;
        self.position += self.speed * delta

        self.matrix = rotmatrix * Matrix().translate(self.position.x,self.position.y,self.position.z)

def make_plane(width, height):
    v4f = (c_float*(width*height*4))()
    width_factor, height_factor = 1.0/float(width), 1.0/float(height)
    for y in xrange(height):
        for x in xrange(width):
            offset = (x+y*width)*4
            v4f[offset:offset+4] = x*width_factor, y*height_factor, -3, 1

    i_width, i_height = width-1, height-1
    indices = (c_uint*(i_width*i_height*4))()
    for y in xrange(i_height):
        for x in xrange(i_width):
            offset = (x+y*i_width)*4
            p1 = x+y*width
            p2 = p1+width
            p4 = p1+1
            p3 = p2+1
            indices[offset:offset+4] = p1, p2, p3, p4

    return VertexObject(
        indices = indices,
        v4f     = v4f,
    )
