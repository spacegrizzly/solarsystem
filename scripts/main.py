import numpy as np
# import utils.data_handler as dh
import data.data as data
from utils.utils import CelestialBody

import pandas as pd


def pandas_wide():
    # import pandas as pd
    desired_width = 200
    pd.set_option('display.width', desired_width)
    # For series
    pd.set_option('display.max_seq_items', None)
    # For DataFrame columns
    pd.set_option('display.max_columns', None)


def main():
    # init
    pandas_wide()

    # create celestial body objects with t0 data
    cb = []
    for i in range(len(data.names)):
        locals()[data.names[i]] = CelestialBody(
            data.names[i],
            data.mass[i],
            data.position[i][0], data.position[i][1], data.position[i][2],
            data.deltav[i][0], data.deltav[i][1], data.deltav[i][2]
        )

        cb.append(locals()[data.names[i]].__dict__)

    cb = pd.DataFrame(cb)
    cb.index = cb.name
    cb = cb.drop(columns=["name"])
    print("\n\nInitial Parameters:\n", cb)

    return 0


def integrate():
    pass


if __name__ == '__main__':
    main()
