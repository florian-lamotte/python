import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "stats.csv",
    sep=";",
    parse_dates=["DATE"],
    date_format="%d/%m/%Y"
)

# FIGURE 1
plt.figure(1, figsize=(12, 5))

plt.plot(
    df["DATE"],
    df["NB"],
    marker="o",
    color="royalblue"
)

plt.title("Evolution du nombre - Courbe")
plt.xlabel("Date")
plt.ylabel("Nombre")
plt.grid(True)

# FIGURE 2
plt.figure(2, figsize=(12, 5))

plt.bar(
    df["DATE"],
    df["NB"],
    color="orange"
)

plt.title("Evolution du nombre - Histogramme")
plt.xlabel("Date")
plt.ylabel("Nombre")
plt.grid(axis="y")

plt.show()