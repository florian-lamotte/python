import typer

app = typer.Typer(
    name="pyforge",
    help="Python Project Generator",
    add_completion=True,
)

@app.command()
def version():
    """Affiche la version."""
    print("PyForge 0.1.0")

if __name__ == "__main__":
    app()