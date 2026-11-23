import csv
from pathlib import Path
from typing import Any

class CSVManager:
    """ Utilitaire de gestion des fichiers CSV. """
    
    def __init__(self, file_path: str | Path, delimiter: str = ";"):
        self.file_path = Path(file_path)
        self.delimiter = delimiter
    
    def csv_exists(self) -> bool:
        """ Vérifie si le fichier CSV existe. """
        return self.file_path.is_file()
    
    def create_csv(
        self,
        headers: list[str],
        rows: list[dict[str, Any]] | None = None
    ) -> None:
        """ Crée un fichier CSV avec ses en-têtes et ses données. """

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open(
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=headers,
                delimiter=self.delimiter
            )

            writer.writeheader()

            if rows:
                writer.writerows(rows)
    
    def read_csv(self) -> list[dict[str, str]]:
        """ Lit le fichier CSV. """

        if not self.csv_exists():
            raise FileNotFoundError(self.file_path)

        with self.file_path.open(
            mode="r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(
                file,
                delimiter=self.delimiter
            )
            return list(reader)
    
    def delete_csv(self) -> bool:
        """ Supprime le fichier CSV. """

        if not self.csv_exists():
            return False

        self.file_path.unlink()
        return True
    
    def get_row(
        self,
        column: str,
        value: Any
    ) -> dict[str, str] | None:
        """ Récupère la première ligne correspondant au critère. """

        rows = self.read_csv()

        for row in rows:
            if row.get(column) == str(value):
                return row

        return None
    
    def append_row(self, row: dict[str, Any]) -> None:
        """ Ajoute une nouvelle ligne au fichier CSV. """

        if not self.csv_exists():
            raise FileNotFoundError(self.file_path)

        with self.file_path.open(
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=self._get_headers(),
                delimiter=self.delimiter
            )
            writer.writerow(row)
    
    def update_row(
        self,
        column: str,
        value: Any,
        updates: dict[str, Any]
    ) -> bool:
        """ Modifie la première ligne correspondant au critère. """

        rows = self.read_csv()
        headers = self._get_headers()

        updated = False

        for row in rows:
            if row.get(column) == str(value):
                row.update({
                    key: str(val)
                    for key, val in updates.items()
                })
                updated = True
                break

        if updated:
            self._write_rows(headers, rows)

        return updated

    def delete_row(
        self,
        column: str,
        value: Any
    ) -> bool:
        """ Supprime la première ligne correspondant au critère. """

        rows = self.read_csv()
        headers = self._get_headers()

        filtered_rows = [
            row for row in rows
            if row.get(column) != str(value)
        ]

        if len(filtered_rows) == len(rows):
            return False

        self._write_rows(headers, filtered_rows)
        return True
    
    def _get_headers(self) -> list[str]:
        """ Récupère les en-têtes du fichier CSV. """

        with self.file_path.open(
            mode="r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.reader(
                file,
                delimiter=self.delimiter
            )
            return next(reader, [])
    
    def _write_rows(
        self,
        headers: list[str],
        rows: list[dict[str, Any]]
    ) -> None:
        """ Réécrit le fichier CSV. """

        with self.file_path.open(
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=headers,
                delimiter=self.delimiter
            )
            writer.writeheader()
            writer.writerows(rows)