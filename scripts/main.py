import copy
import pathlib as pl

from data.raw import data as data
from utils.utils import CelestialBody

from dotenv import dotenv_values
import numpy as np
import pandas as pd


def pandas_wide():
    # import pandas as pd
    desired_width = 200
    pd.set_option('display.width', desired_width)
    # For series
    pd.set_option('display.max_seq_items', None)
    # For DataFrame columns
    pd.set_option('display.max_columns', None)


def show_df(cb_list):
    df_cb = pd.DataFrame(cb_list)
    df_cb.index = df_cb.name
    df_cb = df_cb.drop(columns=["name"])
    print("\n\nInitial Parameters:\n", df_cb)
    return 0


def log_position(cb, lst):
    lst.append(copy.copy(cb.__dict__))
    return 0


def calculate_accelatation(cb, cb_all):
    # create list that contains all objects except cb
    other_cbs = [item for item in cb_all if item.name != cb.name]

    # calculate the acceleration
    a = [0., 0., 0.]
    for other_cb in other_cbs:
        diff = cb.position() - other_cb.position()
        a += other_cb.mass / (np.linalg.norm(diff) * np.linalg.norm(diff)) * (diff / np.linalg.norm(diff))

    a = - data.G * a

    # assign the results to the object
    cb.x_acc = a[0]
    cb.y_acc = a[1]
    cb.z_acc = a[2]

    return 0


def integrate():
    pass


def calculate_new_velocity(cb, dt):
    cb.x_deltav = cb.x_deltav + dt * cb.x_acc
    cb.y_deltav = cb.y_deltav + dt * cb.y_acc
    cb.z_deltav = cb.z_deltav + dt * cb.z_acc
    return 0


def calculate_new_position(cb, dt):
    cb.x_pos = cb.x_pos + dt * cb.x_deltav
    cb.y_pos = cb.y_pos + dt * cb.y_deltav
    cb.z_pos = cb.z_pos + dt * cb.z_deltav
    return 0


def plot(df, config, export):
    import plotly.graph_objects as go
    # template = "simple_white"
    template = "plotly_dark"
    fig = go.Figure()
    fig.update_layout(title="",
                      xaxis_title="x (au)",
                      yaxis_title="y (au)",
                      template=template)

    # Define features
    names = list(df.name.unique())
    colours = list(df.colour.unique())
    dfs = [df[df.name == u] for u in names]

    # Add traces
    for i, df_ in enumerate(dfs):
        # Add lines
        fig.add_trace(
            go.Scattergl(x=df_.x_pos, y=df_.y_pos,
                         mode='lines',
                         name=names[i],
                         line=dict(color=colours[i], dash="solid"),
                         # showlegend=False
                         ))

        # Add markers for the last position in the df
        # scattergl()
        df_ = df_.tail(1)
        size = df_.dummy_size
        fig.add_trace(
            go.Scattergl(x=df_.x_pos, y=df_.y_pos,
                         mode='markers',
                         name=names[i],
                         marker=dict(color=colours[i], size=size),
                         ))

    # fig.update_xaxes(range=(-10, 10))
    # fig.update_yaxes(range=(-10, 10))

    if export:
        path_out = pl.Path(config["path_out"], "plot.html")
        path_out.parent.mkdir(exist_ok=True)
        fig.write_html(str(path_out))

    fig.show()
    return 0


def animate(df, limiting_factor, config, export):
    # import and define default
    import plotly.express as px
    template = "plotly_dark"
    colours = list(df.colour.unique())

    # filter the data to decrease animation time
    df = df[df.index < np.ceil(len(df) * limiting_factor)]
    include = ["Sun", "Mercury", "Venus", "Earth", "Mars"]
    df = df[df.name.isin(include)]
    range_lim = 1.4
    # create scatter plot
    fig = px.scatter_3d(data_frame=df, x="x_pos", y="y_pos", z="z_pos",
                        animation_frame="time",
                        animation_group="name",
                        size="dummy_size",
                        color="name",
                        hover_name="name",
                        range_x=[-range_lim, range_lim],
                        range_y=[-range_lim, range_lim],
                        range_z=[-range_lim, range_lim],
                        color_discrete_sequence=colours,
                        )

    fig.update_layout(template=template)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 0.001

    if export:
        path_out = pl.Path(config["path_out"], "animate.html")
        path_out.parent.mkdir(exist_ok=True)
        fig.write_html(str(path_out))

    fig.show()


def main():
    # init
    pandas_wide()
    config = dotenv_values(".env")

    # create celestial body objects with t0 data
    cbs = []
    cb_list = []
    for i in range(len(data.names)):
        globals()[data.names[i]] = CelestialBody(
            data.names[i],
            data.mass[i],
            data.dummy_sizes[i],
            data.colour[i],
            data.position[i][0], data.position[i][1], data.position[i][2],
            data.deltav[i][0], data.deltav[i][1], data.deltav[i][2],
            0., 0., 0.
        )

        cbs.append(globals()[data.names[i]])
        cb_list.append(globals()[data.names[i]].__dict__)

    show_df(cb_list)

    lst = []
    dt = 0.25
    for time in np.arange(0, 100, dt):
        for cb in cbs:
            calculate_accelatation(cb, cbs)
            calculate_new_velocity(cb, dt)
            calculate_new_position(cb, dt)
            cb.time = time
            log_position(cb, lst)

    df = pd.DataFrame(lst)
    print(3 * "\n", df)

    # plotting options
    plot(df, config=config, export=True)
    animate(df, 0.25, config=config, export=True)

    return 0


if __name__ == '__main__':
    main()
