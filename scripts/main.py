import copy
import pathlib as pl

from data.raw import data as data
from utils.utils import CelestialBody
from utils.integrators import EulerIntegrator, LeapFrogIntegrator

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


def create_energy_dfs(df):
    """
    Extract the cumulative information of the system energy from the log of the simulation

    :param df: pd.DataFrame, logged time-development of the celestial bodies
    :return: 3 pd.DatFrames, for the kin. energy, the pot. energy and the total energy
    """
    # Define features
    names = list(df.name.unique())
    dfs = [df[df.name == u] for u in names]

    # Kinetic energy
    df_e_kin = pd.DataFrame()
    for i, df_ in enumerate(dfs):
        if i == 0:
            df_e_kin = pd.DataFrame(df_.time.loc[:].copy(deep=True)).reset_index()
            df_ = df_.reset_index()
            df_e_kin[names[i]] = df_.e_kin
            df_e_kin = df_e_kin[["time", names[i]]]
        else:
            df_ = df_.reset_index()
            df_e_kin[names[i]] = df_.e_kin

    df_e_kin["e_kin"] = df_e_kin.sum(axis=1) - df_e_kin.time

    # Potential energy
    df_e_pot = pd.DataFrame()
    for i, df_ in enumerate(dfs):
        if i == 0:
            df_e_pot = pd.DataFrame(df_.time.loc[:].copy(deep=True)).reset_index()
            df_ = df_.reset_index()
            df_e_pot[names[i]] = df_.e_pot
            df_e_pot = df_e_pot[["time", names[i]]]
        else:
            df_ = df_.reset_index()
            df_e_pot[names[i]] = df_.e_pot

    df_e_pot["e_pot"] = df_e_pot.sum(axis=1) - df_e_pot.time

    # Total Energy
    df_e_tot = df_e_kin.copy(deep=True)
    df_e_tot = df_e_tot[["time", "e_kin"]]
    df_e_tot["e_pot"] = df_e_pot["e_pot"]
    df_e_tot["e_tot"] = df_e_tot["e_kin"] + df_e_tot["e_pot"]
    print(df_e_tot)

    return df_e_kin, df_e_pot, df_e_tot


def plot_position(df, config, export):
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
            go.Scattergl(x=[i[0] for i in df_.position], y=[i[1] for i in df_.position],
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
            go.Scattergl(x=[i[0] for i in df_.position], y=[i[1] for i in df_.position],
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
    fig = px.scatter_3d(data_frame=df,
                        x=[i[0] for i in df.position], y=[i[1] for i in df.position], z=[i[2] for i in df.position],
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


def plot_energy(df, df_e_tot, config, export):
    import plotly.graph_objects as go
    template = "plotly_dark"
    fig = go.Figure()
    fig.update_layout(title="",
                      xaxis_title="Time",
                      yaxis_title="Kinetic Energy, Potential Energy, Total Energy",
                      template=template)

    # Define features
    names = list(df.name.unique())
    colours = list(df.colour.unique())
    dfs = [df[df.name == u] for u in names]

    # Total Energy
    fig.add_trace(
        go.Scattergl(x=df_e_tot["time"], y=df_e_tot["e_tot"],
                     mode="lines",
                     name="Total Energy",
                     line=dict(color=colours[0], dash="solid"),
                     # showlegend=False
                     ))

    # Kinetic Energy
    fig.add_trace(
        go.Scattergl(x=df_e_tot["time"], y=df_e_tot["e_kin"],
                     mode="lines",
                     name="Kinetic Energy",
                     line=dict(color=colours[1], dash="solid"),
                     # showlegend=False
                     ))

    # Potential Energy
    fig.add_trace(
        go.Scattergl(x=df_e_tot["time"], y=df_e_tot["e_pot"],
                     mode="lines",
                     name="Potential Energy",
                     line=dict(color=colours[2], dash="solid"),
                     # showlegend=False
                     ))
    if export:
        path_out = pl.Path(config["path_out"], "plot_energy.html")
        path_out.parent.mkdir(exist_ok=True)
        fig.write_html(str(path_out))

    fig.show()
    return 0


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
            np.array([data.position[i][0], data.position[i][1], data.position[i][2]]),
            np.array([data.velocity[i][0], data.velocity[i][1], data.velocity[i][2]]),
            np.array([0., 0., 0.]),
            np.array([0., 0., 0.]),
        )

        cbs.append(globals()[data.names[i]])
        cb_list.append(globals()[data.names[i]].__dict__)

    show_df(cb_list)

    # chose an integrator
    # integrator = EulerIntegrator()
    integrator = LeapFrogIntegrator()

    lst = []
    dt = 0.25
    for time in np.arange(0, 100_000, dt):

        # print time to console
        if np.mod(time, 200) == 0:
            print(f"time \t\t {time}")

        # loop over all celestial bodies cb
        for cb in cbs:
            # integrate
            integrator.calculate_acceleration(cb, cbs)
            integrator.calculate_velocity(cb, dt)
            integrator.calculate_position(cb, dt)

            # get time
            cb.time = time

            # calculate energy
            cb.e_kin = cb.get_kinetic_energy()
            cb.e_pot = cb.get_potential_energy()
            cb.total_energy = cb.e_kin + cb.e_pot

            # log the current state
            log_position(cb, lst)

    df = pd.DataFrame(lst)
    print(3 * "\n", df)

    # plotting options
    export = True
    plot_position(df, config=config, export=export)
    animate(df, 0.25, config=config, export=export)

    df_e_kin, df_e_pot, df_e_tot = create_energy_dfs(df)
    plot_energy(df, df_e_tot, config=config, export=export)
    return 0


if __name__ == '__main__':
    main()
