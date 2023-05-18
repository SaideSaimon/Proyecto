import csv
import json
import os.path
import pandas as pd
from src.template.utilitis.rutas import FilesGetter
# from rutas import FilesGetter


class JsonsFiles:
    def __init__(self):
        self.files = FilesGetter().get_directory('json', 'jsons')
        self._default = {'config': self._config(), 'users': self._users(),
                         'scores': self._score()}

    @staticmethod
    def _score() -> dict:
        return {"Facil": [{}], "Normal": [{}], "Dificil": [{}]}

    @staticmethod
    def _users() -> dict:
        return {}

    @staticmethod
    def _config() -> dict:
        return {"Facil": {"-time-": 90, "-rounds-": 10, "-correct-": 25,
                          "-incorrect-": 0, "-clues-": 5},
                "Normal": {"-time-": 30, "-rounds-": 10, "-correct-": 50,
                           "-incorrect-": 0, "-clues-": 3},
                "Dificil": {"-time-": 15, "-rounds-": 10, "-correct-": 100,
                            "-incorrect-": 0, "-clues-": 1},
                "Custom": {"-time-": 60, "-rounds-": 5, "-correct-": 200,
                           "-incorrect-": -100, "-clues-": 5}
                }

    def get_json(self, key: str) -> dict:
        """ Retorna el archivo que recibe por parámetro \n
        :param key: valores -> 'config', 'scores', 'users'"""
        if key in self.files.keys():
            with open(self.files[key], "r", encoding="UTF-8") as file:
                return json.load(file)
        else:
            self.files[key] = os.path.join(self.files['root'], f"{key}.json")
            self.set_json(key, self._default[key])
            with open(self.files[key], "r", encoding="UTF-8") as file:
                return json.load(file)

    def set_json(self, key: str, values: dict) -> None:
        with open(self.files[key], "w", encoding="UTF-8") as file:
            json.dump(values, file)


class Registro:
    def __init__(self):
        self.registro = self.abrir('records')

    @staticmethod
    def _headers():
        return ["timestamp", "id", "evento", "usuario", "estado",
                "texto ingresado", "respuesta", "nivel"]

    def abrir(self, key: str):
        files = FilesGetter().get_directory('csv', 'jsons')
        if key in files.keys():
            return open(files[key], "a", encoding="UTF-8")
        else:
            files[key] = os.path.join(files['root'], f"{key}.csv")
            file = open(files[key], "a+", encoding="UTF-8")
            csv.DictWriter(file, fieldnames=self._headers(),
                           lineterminator='\n').writeheader()
            return file

    def set_registro(self, record: dict):
        csv.DictWriter(self.registro, fieldnames=record.keys(),
                       lineterminator="\n").writerow(record)

    def get_registro(self):
        return csv.DictReader(self.registro)

    def cerrar(self):
        self.registro.close()


class CsvFiles:
    def __init__(self):
        self.files = FilesGetter().get_directory('csv', 'datasets')

    @staticmethod
    def get_file(path):
        return pd.read_csv(path, encoding="UTF-8")

    def get_csvs(self) -> dict:
        self.files.pop('root')
        return {key: self.get_file(path)
                for key, path in list(zip(self.files.keys(),
                                          self.files.values()))}
