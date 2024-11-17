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
        fig, ax = plt.subplots(figsize = figsize)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    df.plot(
        ax = ax,
        alpha = 0.5, edgecolor = 'k',
        column = column, categorical = True,
        legend = True, legend_kwds = {'loc': 'upper left'},
    )

    cx.add_basemap(ax, crs = df.crs, source = cx.providers.CartoDB.Positron)
    fig.tight_layout()
    plt.show()
