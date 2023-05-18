import os
import random
import time
import PySimpleGUI as Sg
from uuid import uuid4
from src.template.utilitis.DAO import JsonsFiles, Registro
from src.template.utilitis.random_dataset import Dataset
from typing import List, Dict


class Jugar:
    def __init__(self, level: str, user: str) -> None:
        self.user, self.level, self.id = user, level, uuid4().hex
        self.logs = Registro()
        self.guess = Dataset().get_card()
        self.record = self.make_record()
        self.config = self.get_config()
        self.window = self.make_window(**self.config)

    def get_config(self) -> dict:
        config = JsonsFiles().get_json('config')[self.level]
        config['-act-'] = 0
        config['answer'] = self.make_answers(config['-rounds-'])
        return config

    @staticmethod
    def make_answers(rounds) -> list:
        return [None for i in range(rounds)]

    def make_record(self) -> dict:
        return {"timestamp": self.get_seconds(), "id": self.id,
                "evento": "inicio_partida", "usuario": self.user,
                "estado": "", "texto ingresado": "", "respuesta": "",
                "nivel": self.level}

    def update_record(self, evento: str, estado: str, texto=None,
                      respuesta=None):
        self.record["evento"], self.record["estado"] = evento, estado
        self.record["texto ingresado"] = texto if texto else ""
        self.record["respuesta"] = respuesta if respuesta else ""
        self.logs.set_registro(self.record)

    @staticmethod
    def get_seconds():
        return int(round(time.time()))

    @staticmethod
    def make_top(user: str, level: str, dataset: str) -> List[Sg.Frame]:
        """ Contiene nombre del jugador, nivel y dataset"""
        dataset = dataset[dataset.index("_") + 1:].capitalize()
        color = '#a0855b'
        content = [Sg.Text(f"Temática:{dataset}", grab=True, font="Any 15",
                           background_color=color),
                   Sg.Push(background_color=color),
                   Sg.Text(f"Dificultad: {level}", grab=True, font="Any 15",
                           background_color=color),
                   Sg.Push(background_color=color),
                   Sg.Text(f"Player: {user}", font="Any 15",
                           background_color=color)]
        return [Sg.Frame('', [content], pad=(0, 0), background_color=color,
                         expand_x=True, border_width=0, grab=True)]

    @staticmethod
    def set_answers_frame(lista: List[int]) -> Sg.Frame:
        """ Frame con la cantidad de rondas que indica si las respuestas
        fueron acertadas o no"""
        layout = [
            [Sg.Text(f"{i + 1}:" if resp is None else f"{i + 1}: {resp}")]
            for i, resp in enumerate(lista)]
        return Sg.Frame(' Respuestas', [[Sg.Column(layout)]], expand_x=True,
                        expand_y=True)

    @staticmethod
    def set_labels_clues(clues: list, opc_title: list) -> Sg.Column:
        """ Crea labels de las pistas """
        return Sg.Column([[Sg.Text(f"{opc_title[i]}: \n"
                                   f"   {i + 1}. {clue}", expand_x=True)]
                          for i, clue in enumerate(clues)])

    @staticmethod
    def set_buttons_options(opciones) -> Sg.Column:
        """ Crea los botones que sirven para elegir la opción correcta"""
        return Sg.Column(random.sample(
            [[Sg.Button(f"{ops}", border_width=0, enable_events=True,
                        expand_x=True)]
             for i, ops in enumerate(opciones)], len(opciones)))

    @staticmethod
    def set_time_frame(timer: int) -> Sg.Frame:
        """ Frame para crear el timer de la ronda, por ahora es texto"""
        return Sg.Frame("Tiempo", [[Sg.Push(),
                                    Sg.Text(f"{timer}", font='Any 20',
                                            k='-time-'),
                                    Sg.Push()]],
                        expand_x=True)

    def set_card_frame(self, card: str, rounds: int, clues: list,
                       opcs: list, opc_title: list) -> Sg.Frame:
        """ Frame conjunto de columnas labels y buttons"""
        return Sg.Frame(f"{card}/{rounds}", [[self.set_labels_clues(clues,
                                                                    opc_title)
                                              ],
                                             [self.set_buttons_options(opcs)]],
                        expand_x=True, expand_y=True, k='-card-')

    def make_window(self, **kwargs: Dict[str, str]) -> Sg.Window:
        """ Crea la ventana principal """
        time, rounds, correct, incorrect, c, card, resp = kwargs.values()
        clues, opciones, dataset, opc_title = self.guess
        print(f"correcta: {opciones[-1]}")
        layout = [self.make_top(self.user, self.level, dataset),
                  [[self.set_answers_frame(resp), Sg.Push(),
                    self.set_time_frame(time),
                    Sg.Push(), self.set_card_frame(card, rounds,
                                                   clues, opciones,opc_title)]
                   ],
                  [Sg.Push(), Sg.Button('Pasar', k='-pass-', border_width=0),
                   Sg.Button('Abandonar', k='-exit-', border_width=0)]]
        return Sg.Window("", layout, size=(800, 500),
                         finalize=True,
                         titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         resizable=True)

    def calc_points(self, answer):
        return self.config['-correct-'] \
            if answer == 'V' else self.config['-incorrect-']

    def update_window(self, answer: str, evento,
                      estado, texto, respuesta=None) -> None:
        """ Actualiza los frames de la pantalla conforme avanza en los rounds
        """
        self.window.close()
        self.record["timestamp"] = self.get_seconds()
        self.update_record(evento, estado, texto, respuesta)
        self.guess = Dataset().get_card()
        self.config['answer'][self.config['-act-']] = self.calc_points(answer)
        self.config['-act-'] += 1
        self.window = self.make_window(**self.config)

    def loop(self) -> None:
        """ Permite leer los eventos de la pantalla y actuar
            basándose en el caso."""
        self.logs.set_registro(self.record)
        while True:
            event, values = self.window.read(timeout=250)
            current_time = self.config["-time-"] - (
                    self.get_seconds() - self.record["timestamp"])
            correcta = self.guess[1][-1]
            if event != "__TIMEOUT__":
                print(f"event: {event}, values:{values}")
            match event:
                case Sg.WIN_CLOSED | "-exit-":
                    self.update_record("fin", "abandonada", "-")
                    self.config['answer'] = None
                    break
                case "__TIMEOUT__":
                    if current_time:
                        self.window['-time-'].update(f"{current_time}")
                    else:
                        self.update_window("F", "intento", "timeout", "-",
                                           correcta)
                case _:
                    if event == '-pass-':
                        self.update_window("--", "intento", "paso", "  ",
                                           correcta)
                    else:
                        choice = self.window[event].get_text()
                        print(f"eleccion: {choice}")
                        if choice == correcta:
                            self.update_window("V", "intento", "ok", choice,
                                               correcta)
                        else:
                            self.update_window("F", "intento", "error", choice,
                                               correcta)
            if self.config['-act-'] == self.config['-rounds-']:
                self.update_record("fin", "finalizada", "-")
                break
        self.window.close()
        self.logs.cerrar()
        Puntajes(self.config['answer'], self.level, self.user).loop()


class Puntajes:
    def __init__(self, puntajes, level, user):
        self.score = puntajes
        self.level = level
        self.user = user

    def make_score(self) -> List[List[Sg.Text]]:
        return [[Sg.Text(f"{i}. {points}", expand_x=True)]
                for i, points in enumerate(self.score)]

    def frame_score(self, title) -> List[Sg.Frame]:
        return [Sg.Frame(title, [[Sg.Column(self.make_score())]],
                         expand_x=True)]

    def frame_total(self, title) -> List[Sg.Frame]:
        return [Sg.Frame(title, [[Sg.Text(f"{sum(self.score)}")]],
                         expand_x=True)]

    def window_score(self) -> Sg.Window:
        return Sg.Window(f"{self.level} | {self.user}",
                         [self.frame_score("Respuestas"),
                              self.frame_total("Total"),
                              [Sg.Button("Ok", k='-exit-', expand_x=True)]]
                         , size=(250, 400))

    def write_score(self):
        js = JsonsFiles()
        score = js.get_json('scores')
        score[self.level].append({self.user: sum(self.score)})
        js.set_json('scores', score)
        print(f'escrito. USer {self.user}, score {sum(self.score)}')

    def loop(self) -> None:
        if self.score:
            window = self.window_score()
            while True:
                event, values = window.read()
                if event in (Sg.WIN_CLOSED, "-exit-"):
                    break
            self.write_score()
            window.close()

        else:
            Sg.popup("Partida Abandonada :(", no_titlebar=True)
