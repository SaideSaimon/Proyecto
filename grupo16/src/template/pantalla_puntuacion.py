import operator
import os
from functools import reduce
from operator import itemgetter
import PySimpleGUI as Sg
from src.template.utilitis.DAO import JsonsFiles
from typing import List, SupportsIndex
from collections import Counter


class Puntuacion:

    def __init__(self):
        self._puntuaciones = JsonsFiles().get_json('scores')
        self._window = self.pantalla_puntuacion()

    def get_promedio(self, level):
        scores = self._puntuaciones[level]
        ocurrencias = Counter([user for score in scores
                               for user in score.keys()])
        totales = reduce(operator.add, map(Counter, scores))
        prom = [[user, float(totales[user] / ocurrencias[user])]
                for user in ocurrencias.keys()]
        prom.sort(key=itemgetter(1), reverse=True)
        return prom

    def get_scores(self, level: SupportsIndex) -> List[List]:
        """Retorna una lista de puntajes [usuario, puntaje] según la
        dificultad recibida por parámetro"""

        scores = [[user, score] for log in self._puntuaciones[level]
                  for user, score in log.items()]
        scores.sort(key=itemgetter(1), reverse=True)
        return scores

    @staticmethod
    def make_combo(values: List[str]) -> Sg.Combo:
        """Genera la lista de las dificultades a elegir"""
        return Sg.Combo(values=list(values), readonly=True, enable_events=True,
                        k="-choice-", expand_x=True)

    @staticmethod
    def make_tables() -> Sg.Frame:
        """Genera la tabla con el top 20 de las puntuaciones de la dificultad
           elegida"""
        return Sg.Frame('Puntajes',
                        [[Sg.Table(values=[], k=f"-tabla{i + 1}-",
                                   headings=["Usuario", "Puntuaciones"],
                                   header_border_width=0,
                                   hide_vertical_scroll=True,
                                   expand_x=True, expand_y=True)
                          for i in range(2)]], expand_x=True, expand_y=True)

    def make_frame(self) -> Sg.Frame:
        """Genera el frame de la pantalla puntuación"""
        return Sg.Frame("Dificultad",
                        [[self.make_combo(self._puntuaciones.keys())]],
                        expand_x=True)

    def pantalla_puntuacion(self) -> Sg.Window:
        """Genera la pantalla de puntuaciones"""
        layout = [[[self.make_frame()],
                   [self.make_tables()]],
                  [Sg.Button('Salir', key='-Exit-',
                             size=(10, 1), border_width=0)]]
        return Sg.Window("Puntuacion", layout, size=(500, 450),
                         titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         finalize=True)

    def loop(self) -> None:
        """Inicia el loop de la lectura de los eventos de la pantalla"""
        while True:
            event, values = self._window.read()
            match event:
                case "-choice-":
                    # print(values)
                    scores = self.get_scores(values["-choice-"])[:20]
                    promedios = self.get_promedio(values["-choice-"])[:20]
                    self._window["-tabla1-"].update(values=scores)
                    self._window["-tabla2-"].update(values=promedios)
                case Sg.WIN_CLOSED | "-Exit-":
                    break
        self._window.close()
