import numpy as np
from data.raw import data as data


class EulerIntegrator:
    """
    Using the Leap Frog method, calculate the integrals needed to solve the many-body problem
    """

    def __init__(self):
        pass

    def calculate_acceleration(self, cb, cb_all):
        """
        Calculating the idealised, gravitational acceleration of all celestial bodies cb_all on one
        specific celestial body cb

        @param cb: CelestialBody object
        @param cb_all: List of all CelestialBody objects that are contained in the simulation
        @return: np.ndarray, 3D, new acceleration
        """

        other_cbs = [item for item in cb_all if item.name != cb.name]
        cb.acceleration_old = cb.acceleration

        a = np.array([0., 0., 0.])

        for other_cbs in other_cbs:
            diff = cb.position - other_cbs.position
            a += other_cbs.mass / (np.linalg.norm(diff) * np.linalg.norm(diff)) * (diff / np.linalg.norm(diff))

        a = - data.G * a

        # assign the results to the object
        cb.acceleration = a
        return cb.acceleration

    def calculate_velocity(self, cb, dt: float):
        """
        Calculating the velocity n of a celestial body cb

        @param cb: CelestialBody object
        @param dt: float, timestep of the integration
        @return: np.ndarray, 3D, new velocity
        """
        cb.velocity = cb.velocity + dt * cb.acceleration
        return cb.velocity

    def calculate_position(self, cb, dt: float):
        """
        Calculating the position n of a celestial body cb

        @param cb: CelestialBody object
        @param dt: float, timestep of the integration
        @return: np.ndarray, 3D, new position
        """
        cb.position = cb.position + dt * cb.velocity
        return cb.position


class LeapFrogIntegrator:
    """
    Using the Leap Frog method, calculate the integrals needed to solve the many-body problem
    """

    def calculate_acceleration(self, cb, cb_all):
        """
        Calculating the idealised, gravitational acceleration of all celestial bodies cb_all on one
        specific celestial body cb. This is unchanged from the Euler method.

        @param cb: CelestialBody object
        @param cb_all: List of all CelestialBody objects that are contained in the simulation
        @return: np.ndarray, 3D, new acceleration
        """

        other_cbs = [item for item in cb_all if item.name != cb.name]
        cb.acceleration_old = cb.acceleration

        a = np.array([0., 0., 0.])
        for other_cbs in other_cbs:
            diff = cb.position - other_cbs.position
            a += other_cbs.mass / (np.linalg.norm(diff) * np.linalg.norm(diff)) * (diff / np.linalg.norm(diff))

        a = - data.G * a

        # assign the results to the object
        cb.acceleration = a
        return cb.acceleration

    def calculate_velocity(self, cb, dt: float):
        """
        Calculating the velocity n of a celestial body cb

        @param cb: CelestialBody object
        @param dt: float, timestep of the integration
        @return: np.ndarray, 3D, new velocity
        """
        cb.velocity = cb.velocity + 0.5 * (cb.acceleration + cb.acceleration_old) * dt

        return cb.velocity

    def calculate_position(self, cb, dt: float):
        """
        Calculating the position n of a celestial body cb

        @param cb: CelestialBody object
        @param dt: float, timestep of the integration
        @return: np.ndarray, 3D, new position
        """
        cb.position = cb.position + dt * cb.velocity + 0.5 * cb.acceleration * dt * dt
        return cb.position
