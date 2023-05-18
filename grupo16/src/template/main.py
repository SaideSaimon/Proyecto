import time
import PySimpleGUI as Sg
from uuid import uuid4
from src.template.utilitis.DAO import Registro
from src.template.utilitis.random_dataset import Dataset
from typing import List, SupportsIndex
from functools import reduce
from operator import itemgetter, add
from collections import Counter
from src.template.interfaces import ScreenMenu, ScreenSettings, \
    ScreenScore, ScreenProfiles, Pop, ScreenPlay


class Tools:

    @staticmethod
    def verify(values, funcs, errors):
        k = None
        for val, key in zip(values.values(), values.keys()):
            if not funcs(key, val):
                k = key
                break
        return Pop.error(errors(k)) if k else True

    @staticmethod
    def update_inputs(elements, items) -> None:
        """Carga los elementos recibidos con los items"""
        for element, item in zip(elements, items):
            element.update(item)

    @staticmethod
    def get_seconds():
        return int(round(time.time()))

    @staticmethod
    def conditional(a, condicion, b):
        return a if condicion else b


class Menu(ScreenMenu):

    def __init__(self):
        super().__init__()
        self._window = self.screen()

    def loop(self) -> None:
        """ El loop permite leer los eventos de la pantalla y actuar
        basándose en el caso."""
        screens = {'-perfiles-': "Profiles().loop()",
                   '-configuración-': "Settings().loop()",
                   '-puntaje-': "Scores().loop()",
                   '-jugar-': "Play(level, user).loop() "
                              "if level != '' and user !='' "
                              "else Pop.error('Elija dificultad y Nivel')"}
        while True:
            event, values = self._window.read()
            event = event if event else '-salir-'
            if event in screens.keys():
                level, user = values['-difficulty-'], values['-user-']
                self._window.close()
                eval(screens[event])
                self._window = self.screen()
            elif event == '-salir-':
                break
        self._window.close()


class Play(Tools, ScreenPlay):
    update = {'window': "self.update_window(*casos['evento'][key], *extra)",
              'record': "self.update_record(*casos['evento'][event])"}

    evaluar = {
        'timeout': "self.window['-time-'].update(f'Tiempo: {current_time}')",
        'respuesta': "self.conditional([event, [correcta]], "
                     "event in ('-pasar-', '__TIMEOUT__'), "
                     "self.conditional(['-ok-', [event[1:-1] ,correcta]], "
                     "event[1:-1]== correcta, "
                     "['-error-', [event[1:-1], correcta]]))",
        'current_time': "self.settings['-time-'] - (self.get_seconds() "
                        "- self.record['timestamp'])",
        'fin': "self.settings['-act-'] == self.settings['-rounds-']"}

    eventos = {'-abandonar-': ['fin', 'abandonada'],
               '-fin-': ['fin', 'finalizada'], '-ok-': ['intento', 'ok'],
               '__TIMEOUT__': ['intento', 'timeout', '-'],
               '-pasar-': ['intento', 'paso', '-'],
               '-error-': ['intento', 'error']}

    def __init__(self, level: str, user: str) -> None:
        super().__init__(level, user)
        self.user, self.level, self.id = user, level, uuid4().hex
        self.logs = Registro()
        self.guess = Dataset().get_card()
        self.record = self.set_record()
        self.settings = self.set_settings(self.data.config[level])
        self.window = self.screen(self.guess, self.settings)

    @staticmethod
    def set_settings(config) -> dict:
        config['-act-'] = 0
        config['answer'] = [None for _ in range(config['-rounds-'])]
        return config

    def set_record(self) -> dict:
        return {"timestamp": self.get_seconds(), "id": self.id,
                "evento": "inicio_partida", "usuario": self.user,
                "estado": "", "texto ingresado": "", "respuesta": "",
                "nivel": self.level}

    def update_record(self, evento: str, estado: str, texto=None,
                      respuesta=None):
        self.record["timestamp"] = self.get_seconds()
        self.record["evento"], self.record["estado"] = evento, estado
        self.record["texto ingresado"] = texto if texto else ""
        self.record["respuesta"] = respuesta if respuesta else ""
        self.logs.registro = self.record

    def update_window(self, evento, estado, choice, respuesta=None) -> None:
        """ Actualiza los frames de la pantalla conforme avanza en los rounds
        """
        self.window.close()
        points = "self.settings['-correct-'] if choice == respuesta " \
                 "else self.settings['-incorrect-']"
        self.update_record(evento, estado, choice, respuesta)
        self.guess = Dataset().get_card()
        self.settings['answer'][self.settings['-act-']] = eval(points)
        self.settings['-act-'] += 1
        self.window = self.screen(self.guess, self.settings)

    def loop(self) -> None:
        """ Permite leer los eventos de la pantalla y actuar
            basándose en el caso."""
        casos = {'evento': self.eventos, 'update': self.update,
                 'evaluar': self.evaluar}
        self.logs.registro = self.record
        while True:
            event, values = self.window.read(timeout=250)
            current_time = eval(casos['evaluar']['current_time'])
            correcta = self.guess[1][-1].lower()
            if event in ('-abandonar-', None):
                event, self.settings['answer'] = '-abandonar-', None
            elif event == '__TIMEOUT__' and current_time:
                eval(casos['evaluar']['timeout'])
            else:
                key, extra = eval(casos['evaluar']['respuesta'])
                print(f"key: {key}, extra:{extra}")
                eval(casos['update']['window'])
            if eval(casos['evaluar']['fin']) | (event == '-abandonar-'):
                event = event if event == '-abandonar-' else '-fin-'
                eval(casos['update']['record'])
                break
        self.window.close()
        self.logs.close()
        if respuestas := self.settings['answer']:
            self.scores_widget(respuestas, total := sum(respuestas))
            scores = self.data.scores
            scores[self.level].append({self.user: total})
            self.data.scores = scores


class Profiles(Tools, ScreenProfiles):
    def __init__(self):
        super().__init__()
        self._user = self.data.users
        self._window = self.screen()

    def funcs(self, key, val):
        funcs = {'-seleccion-': lambda x: x != '',
                 '-users-': lambda x: x not in self._user,
                 '-genero-': lambda x: x.isalpha(),
                 '-edad-': lambda x: x.isdigit()}
        return funcs[key](val)

    @staticmethod
    def errors(key):
        errors = {'-seleccion-': 'Seleccione un usuario',
                  '-users-': 'Usuario existente',
                  '-genero-': lambda x: f'Entrada "{x[1:-1]}" valor no valido.',
                  '-edad-': lambda x: f'Entrada "{x[1:-1]}" valor no valido.'}
        return errors[key] if key not in ('-genero-', '-edad-') \
            else errors[key](key)

    def loop(self) -> None:
        """ Inicia el loop de la lectura de los eventos de la pantalla """

        while True:
            event, values = self._window.read()
            print("evento: ", event, "valor: ", values)
            match event:
                case '-nuevo-':
                    self._window.close()
                    self._window = self.update_layout()
                case "-seleccion-":
                    usuarios = self._user[values['-seleccion-']]
                    inputs = [self._window[key] for key in usuarios.keys()]
                    self.update_inputs(inputs, list(usuarios.values()))
                case "-aceptar-" | "-guardar-":
                    if self.verify(values, self.funcs, self.errors):
                        key = "values.pop('-users-') if event == '-aceptar-' " \
                              "else values.pop('-seleccion-')"
                        self._user[eval(key)] = values
                        self.data.users = self._user
                        Pop.ok(f'Usuario cargado.')
                        break
                case None | "-salir-":
                    break
        self._window.close()


class Settings(Tools, ScreenSettings):
    def __init__(self):
        super().__init__()
        self._config = self.data.config
        self._window = self.screen()

    @staticmethod
    def funcs(_, val):
        return val.isdigit()

    @staticmethod
    def errors(key):
        error = {'-name-': 'Nombre',
                 '-time-': 'Tiempo límite por ronda',
                 '-rounds-': 'Cantidad de rondas por juego',
                 '-correct-': 'Puntaje respuesta correcta',
                 '-incorrect-': 'Puntaje respuesta incorrecta',
                 '-clues-': 'Pistas a mostrar'}
        return f"Entrada no valida {error[key]}"

    def check(self, level, values):
        match level:
            case 'Custom':
                return self.verify(values, self.funcs, self.errors)
            case 'Facil' | 'Normal' | 'Dificil':
                return Pop.error('Error nivel no editable')
            case '':
                return Pop.error('Elija un nivel')
            case _:
                return Pop.error('No se puede cambiar el nombre de los niveles')

    @staticmethod
    def set_int(values):
        return {key: int(val) for key, val in values.items()}

    def loop(self) -> None:
        while True:
            event, values = self._window.read()
            match event:
                case '-list-':
                    name = values['-list-']
                    items = [name] + list(self._config[name].values())
                    inputs = [self._window[key] for key in self._labels.keys()]
                    self.update_inputs(inputs, items)
                case '-guardar-':
                    level, _ = values.pop('-name-'), values.pop('-list-')
                    if self.check(level, values):
                        self._config['Custom'] = self.set_int(values)
                        self.data.config = self._config
                case None | "-salir-":
                    break
        self._window.close()


class Scores(Tools, ScreenScore):

    def __init__(self):
        super().__init__()
        self.scores = self.data.scores
        self._window = self.screen()

    def get_promedio(self, level):
        scores = self.scores[level]
        ocurrencias = Counter([user for score in scores
                               for user in score.keys()])
        totales = reduce(add, map(Counter, scores))
        prom = [[user, round(float(totales[user] / ocurrencias[user]), 2)]
                for user in ocurrencias.keys()]
        prom.sort(key=itemgetter(1), reverse=True)
        return prom

    def get_scores(self, level: SupportsIndex) -> List[List]:
        """Retorna una lista de puntajes [usuario, puntaje] según la
        dificultad recibida por parámetro"""
        scores = [[user, score] for log in self.scores[level]
                  for user, score in log.items()]
        scores.sort(key=itemgetter(1), reverse=True)
        return scores

    def loop(self) -> None:
        """Inicia el loop de la lectura de los eventos de la pantalla"""
        while True:
            event, values = self._window.read()
            match event:
                case "-list-":
                    scores = self.get_scores(values["-list-"])[:20]
                    promedios = self.get_promedio(values["-list-"])[:20]
                    elements = [self._window["table-1"],
                                self._window["table-2"]]
                    self.update_inputs(elements, [scores, promedios])
                case Sg.WIN_CLOSED | "-salir-":
                    break
        self._window.close()
