import numpy as np
import copy
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


def add_one(celestialbody):
    celestialbody.x_pos += 1
    celestialbody.y_pos += 1
    celestialbody.z_pos += 1


def plot_(df):
    import plotly.graph_objects as go
    template = "simple_white"
    fig = go.Figure()
    fig.update_layout(title="",
                      xaxis_title="x (au)",
                      yaxis_title="y (au)",
                      template=template)

    # Define names
    names = list(df.name.unique())
    dfs = [df[df.name == u] for u in names]

    # Add traces
    for i, df_ in enumerate(dfs):
        fig.add_trace(go.Scattergl(x=df_.x_pos, y=df_.y_pos,
                                   mode='lines+markers',
                                   name=names[i]))
    fig.show()
    return 0


def plot(df):
    # import
    import plotly.express as px
    import plotly.io as pio

    # init
    template = "simple_white"
    pio.renderers.default = "browser"

    df = df[df.name == "Earth"]

    # plot
    fig = px.scatter(x=df.x_pos, y=df.y_pos,
                     labels=df.name.iloc[0],
                     template=template,
                     title="")

    fig.show()

    # fig = px.imshow(
    #     df[["pred_rmse", "naive_rmse", "da_rmse", "last_real_rmse", "rolling_avg_rmse"]].transpose(),
    #     color_continuous_scale="viridis_r",
    #     labels=dict(color="RMSE"),
    #     zmin=10,
    #     zmax=70,
    #     template=template,
    #     title="Root-mean square error (RMSE) for different benchmarks \t\t\t" + name
    # )


def show_df(cb_list):
    df_cb = pd.DataFrame(cb_list)
    df_cb.index = df_cb.name
    df_cb = df_cb.drop(columns=["name"])
    print("\n\nInitial Parameters:\n", df_cb)
    return 0


def integrate():
    pass


def log_position(cb, lst):
    lst.append(copy.copy(cb.__dict__))
    return 0


def calculate_new_position(cb, dt):
    cb.x_pos = cb.x_pos + dt * cb.x_deltav
    cb.y_pos = cb.y_pos + dt * cb.y_deltav
    cb.z_pos = cb.z_pos + dt * cb.z_deltav
    return 0


def calculate_new_velocity(cb, dt):
    cb.x_deltav = cb.x_deltav + dt * cb.x_acc
    cb.y_deltav = cb.y_deltav + dt * cb.y_acc
    cb.z_deltav = cb.z_deltav + dt * cb.z_acc
    return 0


def status():
    pass


def calculate_accelatation(cb, cb_all):
    # create list that contains all objects except cb
    other_cbs = [item for item in cb_all if item.name != cb.name]

    # calculate the acceleration
    a = [0., 0., 0.]
    for other_cb in other_cbs:
        diff = cb.position() - other_cb.position()
        a +=  other_cb.mass / (np.linalg.norm(diff) * np.linalg.norm(diff)) * (diff / np.linalg.norm(diff))

    a = - data.G * a
    # assign the results to the object
    cb.x_acc = a[0]
    cb.y_acc = a[1]
    cb.z_acc = a[2]

    return 0


def main():
    # init
    pandas_wide()

    # create celestial body objects with t0 data
    cbs = []
    cb_list = []
    for i in range(len(data.names)):
    # for i in range(2):
        globals()[data.names[i]] = CelestialBody(
            data.names[i],
            data.mass[i],
            data.position[i][0], data.position[i][1], data.position[i][2],
            data.deltav[i][0], data.deltav[i][1], data.deltav[i][2],
            0., 0., 0.
        )

        cbs.append(globals()[data.names[i]])
        cb_list.append(globals()[data.names[i]].__dict__)

    show_df(cb_list)

    lst = []
    dt = 0.1
    for time in np.arange(0, 365, dt):
        for cb in cbs:
            calculate_accelatation(cb, cbs)
            calculate_new_velocity(cb, dt)
            calculate_new_position(cb, dt)
            cb.time = time
            log_position(cb, lst)

    df = pd.DataFrame(lst)
    print(df)

    plot_(df)

    return 0


if __name__ == '__main__':
    main()
