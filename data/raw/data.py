"""Initial conditions of the celestial bodies in the solar system"""

# the names of the individual celestial bodies
names = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

# the masses of the individual celestial bodies normalised to the solar mass
mass = [1.0000e00, 1.6600e-7, 2.4476e-6, 3.0032e-6, 3.2268e-7, 9.5425e-4, 2.8572e-4, 4.3643e-5, 5.1486e-5, 6.6060e-9]

# dummy sizes for plotting
dummy_sizes = [25, 7, 7, 7, 7, 7, 7, 7, 7, 7]

# the colours of the individual celestial bodies as hexadecimal values
colour = ["#fffd37", "#acc2d9", "#f0833a", "#03719c", "#fdaa48",
          "#e2ca76", "#ffa756", "#d0fefe", "#069af3", "#ffd8b1"]

# graviational constant
G = 2.959122e-4

# the positions [x, y, z] of the individual celestial bodies
position = [
    [-1.6132380e-03, -2.3674938e-03, -3.4999903e-05],  # Sun
    [3.4942761e-01, 1.0619088e-02, -3.1182970e-02],  # Mercury
    [-5.7685710e-01, 4.2639983e-01, 3.9039256e-02],  # Venus
    [6.8900355e-01, 7.0799513e-01, -5.4762805e-05],  # Earth
    [4.3534005e-01, -1.3548686e+00, -3.9100527e-02],  # Mars
    [1.8147606e+00, 4.7059241e+00, -6.0234633e-02],  # Jupiter
    [-8.2319838e+00, -5.2651142e+00, 4.1915711e-01],  # Saturn
    [1.9916762e+01, 2.3700466e+00, -2.4922728e-01],  # Uranus
    [2.6481558e+01, -1.4076556e+01, -3.2040642e-01],  # Neptune
    [4.9371124e+00, -3.1890424e+01, 1.9843679e+00],  # Pluto
]

# the velocity [v_x, v_y, v_z] of the individual celestial bodies
velocity = [
    [6.0453208e-06, -1.8980631e-06, -1.3060634e-07],  # Sun
    [-6.4674481e-03, 2.9372684e-02, 2.9939160e-03],  # Mercury
    [-1.2159929e-02, -1.6321487e-02, 4.7839154e-04],  # Venus
    [-1.2606830e-02, 1.1932472e-02, -5.3326343e-07],  # Earth
    [1.3851438e-02, 5.5002850e-03, -2.2479471e-04],  # Mars
    [-7.1329432e-03, 3.0767709e-03, 1.4683761e-04],  # Jupiter
    [2.7027945e-03, -4.7129500e-03, -2.5483556e-05],  # Saturn
    [-4.9354675e-04, 3.7222065e-03, 2.0227673e-05],  # Uranus
    [1.4527105e-03, 2.7901455e-03, -9.1342324e-05],  # Neptune
    [3.1711953e-03, -1.4100225e-04, -9.0807325e-04]  # Pluto
]
