import numpy as np


class CelestialBody:

    def __init__(self, name, mass, dummy_size, colour, x_pos, y_pos, z_pos, x_deltav, y_deltav, z_deltav, x_acc, y_acc, z_acc):
        self.name = name
        self.mass = mass
        self.dummy_size = dummy_size
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.x_deltav = x_deltav
        self.y_deltav = y_deltav
        self.z_deltav = z_deltav
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.z_acc = z_acc
        self.time = 0

    def hello(self):
        return "Hello, {}".format(self.name)

    def position(self):
        return np.array([self.x_pos, self.y_pos, self.z_pos])

    def velocity(self):
        return np.array([self.x_deltav, self.y_deltav, self.z_deltav])

    def acceleration(self):
        return np.array([self.x_acc, self.y_acc, self.z_acc])

