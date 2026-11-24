import json
from pathlib import Path
from typing import Any
from threading import RLock

class JSONManager:
    """ Gestionnaire CRUD générique pour les fichiers JSON. """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.lock = RLock()

        self._initialize_file()

    def _initialize_file(self) -> None:
        """ Crée le fichier JSON s'il n'existe pas. """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        """ Lit le contenu du fichier JSON. """
        with self.lock:
            if not self.file_path.exists():
                return []

            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Le fichier JSON doit contenir une liste.")

            return data

    def _write(self, data: list[dict[str, Any]]) -> None:
        """ Écrit les données dans le fichier JSON. """
        with self.lock:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """ Crée un nouvel enregistrement. """
        with self.lock:
            records = self._read()

            if "id" not in data:
                data["id"] = max(
                    (item.get("id", 0) for item in records),
                    default=0
                ) + 1

            if any(item.get("id") == data["id"] for item in records):
                raise ValueError("Cet ID existe déjà.")

            records.append(data)
            self._write(records)

            return data

    def get_all(self) -> list[dict[str, Any]]:
        """ Récupère tous les enregistrements. """
        return self._read()

    def get_by_id(self, record_id: int) -> dict[str, Any] | None:
        """ Récupère un enregistrement par son ID. """
        records = self._read()

        return next(
            (item for item in records if item.get("id") == record_id),
            None
        )

    def update(
        self,
        record_id: int,
        data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """ Met à jour un enregistrement. """
        
        with self.lock:
            records = self._read()

            for index, item in enumerate(records):
                if item.get("id") == record_id:
                    updated = {**item, **data, "id": record_id}
                    records[index] = updated
                    self._write(records)
                    return updated

            return None

    def delete(self, record_id: int) -> bool:
        """ Supprime un enregistrement. """
        
        with self.lock:
            records = self._read()

            filtered = [
                item for item in records
                if item.get("id") != record_id
            ]

            if len(filtered) == len(records):
                return False

            self._write(filtered)
            return True