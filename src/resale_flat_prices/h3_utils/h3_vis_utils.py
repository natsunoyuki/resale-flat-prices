# https://uber.github.io/h3-py/intro.html
# https://uber.github.io/h3-py/polygon_tutorial.html
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as cx


def plot_df(
    df, 
    plot_kwds = {
        "figsize": [8, 8],
        "xlim": None,
        "ylim": None,
        "alpha": 0.5,
        "categorical": False,
        "column": None,
        "legend": True,
        "legend_kwds": {},
        "cmap": 'viridis',
        "edgecolor": None,
        "divider_kwds": {"position": "right", "size": "5%", "pad": 0.1},
    },
):
    """Plot the `geometry` column of a GeoDataFrame."""
    df = df.copy()

    fig, ax = plt.subplots(figsize = plot_kwds.get("figsize"))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(**plot_kwds.get("divider_kwds"))

    if plot_kwds.get("xlim", None) is not None:
        ax.set_xlim(plot_kwds.get("xlim"))
    if plot_kwds.get("ylim", None) is not None:
        ax.set_ylim(plot_kwds.get("ylim"))  
    df.plot(
        ax = ax,
        alpha = plot_kwds.get("alpha"),
        column = plot_kwds.get("column"), 
        categorical = plot_kwds.get("categorical"),
        legend = plot_kwds.get("legend"), 
        legend_kwds = plot_kwds.get("legend_kwds"),
        cmap = plot_kwds.get("cmap"),
        edgecolor = plot_kwds.get("edgecolor"),
        cax = cax,
    )

    cx.add_basemap(ax, crs = df.crs, source = cx.providers.CartoDB.Positron)
    fig.tight_layout()
    plt.show()
