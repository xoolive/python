import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cartopy import crs, feature
from scipy.stats import gaussian_kde

df = pd.read_csv(
    "../../data/villes_france.csv",
    usecols=[5, 19, 20],
    names=["nom", "longitude", "latitude"],
)


def countries(**kwargs):
    params = {
        "category": "cultural",
        "name": "admin_0_countries",
        "scale": "10m",
        "edgecolor": "#524c50",
        "facecolor": "none",
        "alpha": 0.5,
        **kwargs,
    }
    return feature.NaturalEarthFeature(**params)


e = crs.EuroPP()
fig, ax = plt.subplots(2, 2, figsize=(10, 10), subplot_kw=dict(projection=e))


ville_ac = df.query('nom.str.match(".*\w{2}ac(-|$).*")', engine="python")
ville_ay = df.query('nom.str.match(".*\w{2}ay(-|$).*")', engine="python")


for ax_ in ax.ravel():
    ax_.add_feature(countries(scale="50m"))
    ax_.set_extent((-4, 9, 42, 51))

ville_ac.plot.scatter(
    ax=ax[0, 0],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="C3",
)
ville_ay.plot.scatter(
    ax=ax[0, 0],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="C0",
)

ville_ac.plot.scatter(
    ax=ax[0, 1],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="white",
    edgecolor="black",
    s=60,
    zorder=-2,
)
ville_ay.plot.scatter(
    ax=ax[0, 1],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="white",
    edgecolor="black",
    s=60,
    zorder=-2,
)

ville_ac.plot.scatter(
    ax=ax[0, 1],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="white",
    s=30,
    zorder=-2,
)
ville_ay.plot.scatter(
    ax=ax[0, 1],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="white",
    s=30,
    zorder=-2,
)

ville_ac.plot.scatter(
    ax=ax[0, 1],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="C3",
    alpha=0.2,
)
ville_ay.plot.scatter(
    ax=ax[0, 1],
    x="longitude",
    y="latitude",
    transform=crs.PlateCarree(),
    color="C0",
    alpha=0.2,
)

xmin, xmax, ymin, ymax = ax[0, 0].get_extent()

cmap = plt.get_cmap("Blues")
cmap.set_under("none")

x, y, *_ = e.transform_points(
    crs.PlateCarree(),
    ville_ay.longitude.values,
    ville_ay.latitude.values,
).T

h = ax[1, 0].hexbin(
    x, y, extent=[xmin, xmax, ymin, ymax], gridsize=30, cmap=cmap, vmin=1
)

cmap = plt.get_cmap("Reds")
cmap.set_under("none")

x, y, *_ = e.transform_points(
    crs.PlateCarree(),
    ville_ac.longitude.values,
    ville_ac.latitude.values,
).T

h = ax[1, 0].hexbin(
    x, y, extent=[xmin, xmax, ymin, ymax], gridsize=30, cmap=cmap, vmin=1
)

cmap = plt.get_cmap("RdBu")

x, y, *_ = e.transform_points(
    crs.PlateCarree(),
    ville_ay.longitude.values,
    ville_ay.latitude.values,
).T

X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])

values = np.vstack([x, y])
kernel = gaussian_kde(values)

Z = np.reshape(kernel(positions).T, X.shape).T

ax[1, 1].annotate(
    xy=(X.T[np.where(Z == Z.max())][0], Y.T[np.where(Z == Z.max())][0]),
    xytext=(20, -10),
    textcoords="offset points",
    s="-ay",
    fontsize=24,
    fontname="Ubuntu",
    bbox=dict(boxstyle="round", fc="white", ec="white", pad=0.1, alpha=0.5),
)

x, y, *_ = e.transform_points(
    crs.PlateCarree(),
    ville_ac.longitude.values,
    ville_ac.latitude.values,
).T

X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])

values = np.vstack([x, y])
kernel = gaussian_kde(values)

Z -= np.reshape(kernel(positions).T, X.shape).T / 2

ax[1, 1].annotate(
    xy=(X.T[np.where(Z == Z.min())][0], Y.T[np.where(Z == Z.min())][0]),
    xytext=(-30, -30),
    textcoords="offset points",
    s="-ac",
    fontsize=24,
    fontname="Ubuntu",
    bbox=dict(boxstyle="round", fc="white", ec="white", pad=0.1, alpha=0.5),
)

h = ax[1, 1].imshow(
    Z,
    cmap=cmap,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    vmin=-0.75e-11,
    vmax=0.75e-11,
)

fig.subplots_adjust(wspace=0.05, hspace=0.05)
fig.savefig("fig06.png")

plt.show()
