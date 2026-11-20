import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "stats.csv",
    sep=";",
    parse_dates=["DATE"],
    date_format="%d/%m/%Y"
)

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# graphique 1
axes[0].plot(
    df["DATE"],
    df["NB"],
    marker="o",
    color="royalblue"
)

axes[0].set_title("Evolution en courbe")
axes[0].set_ylabel("Nombre")
axes[0].grid(True)

# graphique 2
axes[1].bar(
    df["DATE"],
    df["NB"],
    color="orange"
)

axes[1].set_title("Evolution en histogramme")
axes[1].set_ylabel("Nombre")
axes[1].grid(axis="y")

fig.tight_layout()

plt.show()