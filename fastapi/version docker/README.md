# Création d'un projet avec FastAPI et Docker

[Documentation FastAPI](https://fastapi.tiangolo.com/)

### 1. Créer le fichier main.py
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

### 2. Créer le fichier `requirements.txt`
```
fastapi
uvicorn[standard]
```

### 3. Lancer la construction du conteneur
```
docker build -t nom-du-projet .
```

### 4. Lancer le conteneur
```
docker run --name nom-du-container -p 8000:8000 nom-du-projet
```
Changer `8000:8000` en `8001:8000`, `8002:8000`,... si besoin.  
`docker ps` permet de voir quels conteneurs sont actifs.  
`docker stop NOM_DU_CONTENEUR` arrête un conteneur.

### 5. Ouvrir l'interface web
http://localhost:8000  
http://localhost:8000/docs