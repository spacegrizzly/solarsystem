import numpy as np
from data.raw import data as data


class CelestialBody:
    """
    Create an instance of the class "CelestialBody" that contains physical properties such as the mass, position,
    velocity and acceleration, as well as energy information of the object
    """

    def __init__(self, name: str, mass: str, dummy_size: float, colour: str,
                 position, velocity, acceleration, acceleration_old):
        self.name = name
        self.mass = mass
        self.dummy_size = dummy_size
        self.colour = colour
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.acceleration_old = acceleration_old
        self.e_kin = 0.
        self.e_pot = 0.
        self.total_energy = 0.
        self.time = 0.

        # check whether the input variables comply with the requirements
        lst_check = {"position": self.position,
                     "velocity": self.velocity,
                     "acceleration": self.acceleration,
                     "acceleration_old": self.acceleration_old
                     }

        for key in lst_check:
            if not isinstance(lst_check[key], np.ndarray):
                raise TypeError(f"{key}: Input variable not of type np.ndarray")
            if not lst_check[key].shape[0] == 3:
                raise TypeError(f"{key}: Numpy array not of shape (3,)")

    def hello(self):
        return f"Hello, {self.name} :)"

    def get_kinetic_energy(self) -> float:
        """
        Calculate the kinetic energy of the celestial body
        """
        e_kin = self.mass * self.velocity.dot(self.velocity) / 2.
        return e_kin

    def get_potential_energy(self) -> float:
        e_pot = - data.G * self.mass * (np.sum(data.mass) - self.mass) / np.linalg.norm(self.position)
        return e_pot
