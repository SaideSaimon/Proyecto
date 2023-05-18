import random
from src.template.utilitis.DAO import CsvFiles

class Dataset:
    def __init__(self):
        self._sets = CsvFiles().get_csvs()
        self._dataset = self.get_random_dataset()

    def get_random_dataset(self):
        """ Obtiene la clave del dataset en forma random"""
        return random.choice(list(self._sets.keys()))

    def get_card(self):
        """ Genera una lista [pistas:list, opciones:list, dataset:str]"""
        frame = self._sets[self._dataset]
        selected_rows = frame.sample(5).values.tolist()
        headers = list(frame.keys())[:-1]
        return [selected_rows[-1], [option.pop() for option in selected_rows],
                self._dataset] + [headers]
