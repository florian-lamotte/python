import typer
from rich import print

app = typer.Typer()

@app.command()
def init(
    name: str,
):
    print(f"Création du projet : {name}")