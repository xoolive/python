import matplotlib.pyplot as plt
from cartopy import crs, feature
from matplotlib.transforms import offset_copy

fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(131, projection=crs.Mercator())
ax2 = fig.add_subplot(132, projection=crs.Orthographic(0, 60))
ax4 = fig.add_subplot(133, projection=crs.EuroPP())

for ax_ in [ax1, ax2, ax4]:
    # Données du projet Natural Earth (disponibles au 10, 50 et 110 millionièmes)
    ax_.add_feature(feature.COASTLINE.with_scale("50m"))
    ax_.plot(  # dans l'ordre longitude, latitude
        6.865,
        45.832778,
        marker="o",
        color="black",
        transform=crs.PlateCarree(),
    )

    geodetic_transform = crs.PlateCarree()._as_mpl_transform(ax_)
    text_transform = offset_copy(geodetic_transform, units="dots", x=15)

    ax_.text(
        6.865,
        45.832778,
        "Mont Blanc",
        fontsize=14,
        fontname="Ubuntu",
        bbox=dict(boxstyle="round", facecolor="w", edgecolor="k", lw=2),
        transform=text_transform,
    )
    ax_.set_global()

style = dict(fontname="Ubuntu", fontsize=16, pad=15)
ax1.set_title("projection=crs.Mercator()", **style)
ax2.set_title("projection=crs.Orthographic(0, 60)", **style)
ax4.set_title("projection=crs.EuroPP()", **style)

fig.savefig("fig17.png", bbox_inches="tight")
plt.show()