# https://uber.github.io/h3-py/intro.html
# https://uber.github.io/h3-py/polygon_tutorial.html
import h3
import matplotlib.pyplot as plt
import geopandas
import contextily as cx


def plot_df(df, column = None, ax = None, figsize = [8, 8], epsg = 3857):
    "Plot based on the `geometry` column of a GeoPandas dataframe"
    df = df.copy()
    df = df.to_crs(epsg = epsg)

    if ax is None:
        _, ax = plt.subplots(figsize = figsize)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    df.plot(
        ax = ax,
        alpha = 0.5, edgecolor = 'k',
        column = column, categorical = True,
        legend = True, legend_kwds = {'loc': 'upper left'},
    )

    cx.add_basemap(ax, crs = df.crs, source = cx.providers.CartoDB.Positron)
    plt.show()


def plot_shape(shape, ax = None, crs = 'EPSG:4326'):
    df = geopandas.GeoDataFrame({'geometry': [shape]}, crs = crs)
    plot_df(df, ax = ax)


def plot_cells(cells, ax = None):
    shape = h3.cells_to_h3shape(cells)
    plot_shape(shape, ax = ax)


def plot_shape_and_cells(shape, res = 9):
    fig, axs = plt.subplots(1, 2, figsize = (10, 5), sharex = True, sharey = True)
    plot_shape(shape, ax = axs[0])
    plot_cells(h3.h3shape_to_cells(shape, res), ax = axs[1])
    fig.tight_layout()