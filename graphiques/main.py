import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "stats.csv",
    sep=";",
    parse_dates=["DATE"],
    date_format="%d/%m/%Y"
)

print(df)

# taille du graphique (12 pouces de large, 6 de haut)
plt.figure(figsize=(12, 6))

# tracé de la courbe
plt.plot(
    df["DATE"], # axe horizontal x
    df["NB"], # axe vertical y
    marker="o", # forme du marqueur (optionnel)
    markersize=8, # taille des marqueurs
    linewidth=2, # épaisseur du tracé
    color="royalblue", # couleur du tracé
    label="Nombre" # nom de la courbe (pour la légende)
)

plt.title("Évolution du nombre par date", fontsize=16)
plt.xlabel("Dates", fontsize=12)
plt.ylabel("Nombres", fontsize=12)

# grille (affichage, style des lignes, transparence des lignes)
plt.grid(True, linestyle="--", alpha=0.5)

# inclinaison des libellés de l'axe horizontal
plt.xticks(rotation=45)

# affichage de la légende
plt.legend()

# ajuste les marges
plt.tight_layout()

# Affichage
plt.show()