
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk

from tkinter import filedialog, ttk, messagebox

CONFIG = {
    "separateur_csv": ";",
    "taille_graphique": (12, 6),
    "couleurs": [
        "royalblue",
        "red",
        "green",
        "orange",
        "purple",
        "brown",
        "magenta",
        "darkcyan"
    ],
    "taille_marqueur": 8,
    "epaisseur_ligne": 2,
    "rotation_x": 45
}

def selectionner_fichier():
    # ouvre la fenêtre de sélection du fichier
    root = tk.Tk()
    root.withdraw()

    fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier CSV",
        filetypes=[
            ("Fichiers CSV", "*.csv"),
            ("Tous les fichiers", "*.*")
        ]
    )

    return root, fichier

def charger_donnees(fichier):
    try:
        df = pd.read_csv(fichier, sep=CONFIG["separateur_csv"])

        if df.empty:
            raise ValueError("Le fichier CSV est vide.")

        return df

    except Exception as erreur:
        messagebox.showerror("Erreur de lecture", str(erreur))
        
        return None

def configurer_graphique(root, df):
    fenetre = tk.Toplevel(root)
    fenetre.title("Choix des colonnes")
    fenetre.geometry("350x350")

    resultat = {}

    # ----- colonne x -----
    ttk.Label(
        fenetre,
        text="Colonne pour l'axe X (horizontal) :"
    ).pack(pady=5)

    choix_x = ttk.Combobox(
        fenetre,
        values=list(df.columns),
        state="readonly"
    )

    choix_x.pack()
    choix_x.current(0)

    # ----- colonnes y -----
    ttk.Label(
        fenetre,
        text="Colonnes pour l'axe Y (vertical) :"
    ).pack(pady=5)

    # conteneur des listes déroulantes
    cadre_courbes = tk.Frame(fenetre)
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
        choix.current(
            min(len(choix_courbes) + 1, len(df.columns) - 1)
        )

        choix_courbes.append(choix)

    # la pemière courbe est obligatoire
    ajouter_courbe()

    # ajout d'une courbe
    ttk.Button(
        fenetre,
        text="+ Ajouter une courbe",
        command=ajouter_courbe
    ).pack(pady=5)

    # ----- titre du graphique -----
    ttk.Label(
        fenetre,
        text="Titre du graphique :"
    ).pack(pady=5)

    champ_titre = tk.Entry(fenetre, width=40)
    champ_titre.pack()

    # ----- bouton de validation -----
    def valider():
        resultat["x"] = choix_x.get()

        resultat["y"] = [
            choix.get()
            for choix in choix_courbes
            if choix.get()
        ]

        resultat["titre"] = champ_titre.get()

        if not resultat["y"]:
            messagebox.showwarning(
                "Attention",
                "Sélectionne au moins une colonne Y."
            )
            return

        fenetre.destroy()

    ttk.Button(
        fenetre,
        text="Valider",
        command=valider
    ).pack(pady=15)

    # attend la validation
    root.wait_window(fenetre)

    return resultat if resultat else None

def tracer_graphique(df, configuration):
    colonne_x = configuration["x"]
    colonnes_y = configuration["y"]
    titre = configuration["titre"]

    # taille du graphique en pouces (largeur, hauteur)
    plt.figure(figsize=CONFIG["taille_graphique"])

    # tracé de la courbe
    for i, colonne_y in enumerate(colonnes_y):
        couleur = CONFIG["couleurs"][
            i % len(CONFIG["couleurs"])
        ]

        plt.plot(
            df[colonne_x], # axe horizontal x
            df[colonne_y], # axe vertical y
            marker="o", # forme du marqueur (optionnel)
            markersize=CONFIG["taille_marqueur"], # taille des marqueurs
            linewidth=CONFIG["epaisseur_ligne"], # épaisseur du tracé
            color=couleur, # couleur du tracé
            label=colonne_y # nom de la courbe (pour la légende)
        )

    plt.title(titre, fontsize=16)
    plt.xlabel(colonne_x, fontsize=12)
    plt.ylabel("Valeurs", fontsize=12)

    # grille (affichage, style des lignes, transparence des lignes)
    plt.grid(True, linestyle="--", alpha=0.5)

    # inclinaison des libellés de l'axe horizontal
    plt.xticks(rotation=CONFIG["rotation_x"])

    # affichage de la légende
    plt.legend()
    
    # ajuste les marges
    plt.tight_layout()

def main():
    root, fichier = selectionner_fichier()

    if not fichier:
        print("Aucun fichier sélectionné.")
        root.destroy()
        return

    df = charger_donnees(fichier)

    if df is None:
        root.destroy()
        return

    configuration = configurer_graphique(root, df)

    root.destroy()

    if configuration is None:
        return

    try:
        tracer_graphique(df, configuration)
        plt.show()

    except Exception as erreur:
        messagebox.showerror("Erreur graphique", str(erreur))

if __name__ == "__main__":
    main()
