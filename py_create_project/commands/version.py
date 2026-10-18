import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def version():
    print("PyForge 0.1.0")