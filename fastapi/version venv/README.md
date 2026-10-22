# Création d'un projet avec FastAPI

[Documentation FastAPI](https://fastapi.tiangolo.com/)

### 1. Créer un environnement virtuel
Lancer cette commande :
```
python -m venv .venv
```

### 2. Installer FastAPI
Lancer cette commande avec PowerShell :
```
.\.venv\Scripts\python.exe -m pip install "fastapi[standard]"
```

### 3. Créer le fichier main.py
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### 4. Démarrer le serveur de développement
Lancer cette commande :
```
fastapi dev
```

### 5. Ouvrir l'interface web
http://127.0.0.1:8000  
http://127.0.0.1:8000/docs