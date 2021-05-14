class CelestialBody:

    def __init__(self, name, mass, x_pos, y_pos, z_pos, x_deltav, y_deltav, z_deltav):
        self.name = name
        self.mass = mass
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.x_deltav = x_deltav
        self.y_deltav = y_deltav
        self.z_deltav = z_deltav

    def hello(self):
        return "Hello, {}".format(self.name)

    def position(self):
        return [self.x_pos, self.y_pos, self.z_pos]

    def velocity(self):
        return [self.x_deltav, self.y_deltav, self.z_deltav]
