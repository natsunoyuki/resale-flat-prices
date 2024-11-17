# https://uber.github.io/h3-py/intro.html
# https://uber.github.io/h3-py/polygon_tutorial.html
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as cx


def plot_df(
    df, 
    column = None, 
    epsg = 3857,
    figsize = [8, 8], 
    alpha = 0.5,
    categorical = False,
    legend = True,
    legend_kwds = {},
    edgecolor = None,
    divider_kwds = {"position": "right", "size": "5%", "pad": 0.1},
):
    """Plot based on the `geometry` column of a GeoPandas dataframe."""
    df = df.copy()
    df = df.to_crs(epsg = epsg)

    fig, ax = plt.subplots(figsize = figsize)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes(**divider_kwds)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    df.plot(
        ax = ax,
        alpha = alpha,
        column = column, 
        categorical = categorical,
        legend = legend, 
        legend_kwds = legend_kwds,
        edgecolor = edgecolor,
        cax = cax,
    )

    cx.add_basemap(ax, crs = df.crs, source = cx.providers.CartoDB.Positron)
    fig.tight_layout()
    plt.show()
