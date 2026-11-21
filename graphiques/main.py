import pandas as pd
import matplotlib.pyplot as plt

from tkinter import Tk, filedialog, ttk, Toplevel, Label, Button, Entry, Frame

# ouvre la fenêtre de sélection du fichier
root = Tk()
root.withdraw() # masque la fenêtre tkinter

fichier = filedialog.askopenfilename(
    title="Sélectionner un fichier CSV",
    filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
)

if not fichier:
    print("Aucun fichier sélectionné.")
    exit()

df = pd.read_csv(
    fichier,
    sep=";"
)

fenetre = Toplevel(root)
fenetre.title("Choix des colonnes")
fenetre.geometry("350x300")

# ----- colonnes x -----
Label(fenetre, text="Colonnes pour l'axe X (horizontal) :").pack(pady=5)

choix_x = ttk.Combobox(
    fenetre,
    values=list(df.columns),
    state="readonly"
)
choix_x.pack()
choix_x.current(0)

# ----- colonnes y -----
Label(fenetre, text="Colonnes pour l'axe Y (vertical) :").pack(pady=5)

# conteneur des listes déroulantes
cadre_courbes = Frame(fenetre)
cadre_courbes.pack()

# liste des courbes Y
choix_courbes = []

def ajouter_courbe():
    choix = ttk.Combobox(
        cadre_courbes,
        values=list(df.columns),
        state="readonly",
        width=25
    )

    choix.pack(pady=3)

    # sélection automatique d'une colonne disponible
    choix.current(min(len(choix_courbes) + 1, len(df.columns) - 1))

    choix_courbes.append(choix)

# la pemière courbe est obligatoire
ajouter_courbe()

# ajout d'une courbe
Button(
    fenetre,
    text="+ Ajouter une courbe",
    command=ajouter_courbe
).pack(pady=5)

# ----- nom du graphique -----
Label(fenetre, text="Titre du graphique :").pack(pady=5)

champ_titre = Entry(fenetre, width=40)
champ_titre.pack()

champ_titre.insert(0, "") # titre par défaut

# ----- bouton de validation -----
def valider():
    global colonne_x, colonnes_y, titre_graphique

    colonne_x = choix_x.get()
    
    colonnes_y = [
        choix.get()
        for choix in choix_courbes
        if choix.get()
    ]
    
    titre_graphique = champ_titre.get()

    fenetre.destroy()

Button(
    fenetre,
    text="Valider",
    command=valider
).pack(pady=15)

# Attendre la validation
root.wait_window(fenetre)

print(df)

# taille du graphique (12 pouces de large, 6 de haut)
plt.figure(figsize=(12, 6))

couleurs = [
    "royalblue",
    "red",
    "green",
    "orange",
    "purple",
    "brown",
    "magenta",
    "darkcyan"
]

# tracé de la courbe
for i, colonne_y in enumerate(colonnes_y):
    plt.plot(
        df[colonne_x], # axe horizontal x
        df[colonne_y], # axe vertical y
        marker="o", # forme du marqueur (optionnel)
        markersize=8, # taille des marqueurs
        linewidth=2, # épaisseur du tracé
        color=couleurs[i % len(couleurs)], # couleur du tracé
        label=colonne_y # nom de la courbe (pour la légende)
    )

plt.title(titre_graphique, fontsize=16)
plt.xlabel(colonne_x, fontsize=12)
plt.ylabel("Valeurs", fontsize=12)

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