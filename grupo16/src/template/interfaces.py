from functools import reduce
import random
import PySimpleGUI as Sg
from typing import List, Any
from src.template.utilitis.DAO import JsonsFiles


class Data:
    _config: dict = JsonsFiles().get_json('config')
    _users: dict = JsonsFiles().get_json('users')
    _scores: dict = JsonsFiles().get_json('scores')

    @property
    def config(self) -> dict:
        return self._config

    @config.setter
    def config(self, values):
        JsonsFiles().set_json('config', values)

    @property
    def users(self) -> dict:
        return self._users

    @users.setter
    def users(self, values):
        JsonsFiles().set_json('users', values)

    @property
    def scores(self) -> dict:
        return self._scores

    @scores.setter
    def scores(self, values):
        JsonsFiles().set_json('scores', values)


class Interface:
    def __init__(self):
        self.data = Data()

    @staticmethod
    def sep(cant, color=None) -> List[Sg.Push()]:
        return [Sg.Push(background_color=color) for _ in range(cant)]

    @staticmethod
    def labels(labels, color=None, font=None) -> List[Sg.Text]:
        """ Crea los textos a la izquierda del input """
        return [Sg.Text(label, background_color=color, font=font)
                for label in labels]

    @staticmethod
    def buttons(tittles: list) -> List[List[Sg.Button()]]:
        """ Crea una lista de botones"""
        return [[Sg.Button(title, k=f"-{title.lower()}-",
                           border_width=0, size=(20, 1))]
                for title in tittles]

    @staticmethod
    def inputs(keys) -> List[Sg.InputText]:
        """ Crea los inputs """
        return [Sg.InputText(size=(17, 1), k=key, justification='right')
                for key in keys]

    @staticmethod
    def combo(values: list, key: str) -> Sg.Combo:
        """ Crea la lista desplegable de usuarios o niveles \n
        :param values: Contenido del desplegable
        :param key: Clave asignada al Combo"""
        return Sg.Combo(values=values, readonly=True, enable_events=True,
                        k=key, size=(15, 1))

    @staticmethod
    def column(elements, key=None) -> Sg.Column:
        return Sg.Column(elements, k=key, expand_y=True)

    @staticmethod
    def frame(label, *args, y=False, x=False, color=None) -> List[Sg.Frame]:
        # for arg in args[0]:
        #     print(type(arg))
        return [Sg.Frame(label, [[arg for arg in args[0]]],
                         expand_x=x, expand_y=y, background_color=color,
                         element_justification='center')]

    @staticmethod
    def table(key: str, headers: list, values: list):
        return Sg.Table(values=values, k=key, headings=headers,
                        header_border_width=0, hide_vertical_scroll=True,
                        expand_x=True, expand_y=True)

    @staticmethod
    def menu(layout) -> Sg.Window:
        """ Crea el menu de configuración"""
        Sg.theme_global('LightBrown11')
        return Sg.Window("", layout, size=(600, 525),
                         element_justification='center',
                         finalize=True)

    def zip_labels_inputs(self, list_labels, sep, list_inputs) -> List[Any]:
        labels, sep = self.labels(list_labels), self.sep(sep)
        inputs = self.inputs(list_inputs)
        return list(map(list, zip(labels, sep, inputs)))

    def horizontal_bttns(self, buttons) -> List[Sg.Button]:
        return reduce(lambda x, y: x + y, self.buttons(buttons))


class ScreenMenu(Interface):

    def __init__(self):
        super().__init__()

    def screen(self):
        tittles = ["Jugar", "Perfiles", "Configuración", "Puntaje", "Salir"]
        buttons = self.column(self.buttons(tittles), key=None)
        frame = self.frame(f"{' ' * 7}Dificultad{' ' * 25}Usuario{' ' * 5}",
                           [self.combo(list(self.data.config.keys()),
                                       "-difficulty-"),
                            self.combo(list(self.data.users.keys()), "-user-")])
        return self.menu([[Sg.VPush()], [buttons], [frame]])


class ScreenPlay(Interface):
    def __init__(self, level, user):
        super().__init__()
        self.level, self.user = level, user

    def screen(self, guess, settings):
        time, rounds, correct, incorrect, c, card, resp = settings.values()
        clues, opciones, dataset, opc_title = guess
        print(f"correcta: {opciones[-1]}")
        dataset = dataset[dataset.index('_') + 1:].capitalize()
        layout = [self.top(dataset, time), self.replied(resp),
                  self.clues(card, rounds, clues, opciones, opc_title),
                  [Sg.VPush()], self.action()]
        return self.menu(layout)

    def scores_widget(self, scores, total):
        column = self.column(self.labels([f"{i + 1}. {points}"])
                             for i, points in enumerate(scores))
        puntajes = self.frame(f"Player: {self.user}  |  "
                              f"Nivel: {self.level}", [column], x=True)
        total = self.frame("Total", self.labels([f"{total}"]), x=True)
        accion = self.buttons(['Salir'])[0]
        layout = [[Sg.VPush()], puntajes, total, accion, [Sg.VPush()]]
        window = self.menu(layout)
        window.read()
        window.close()

    def top(self, dataset, time):
        color = '#a0855b'
        labels, sep = self.labels([f"Temática: {dataset}",
                                   f"Usuario: {self.user}",
                                   f"Nivel: {self.user}"],
                                  color, font='Any 10'), self.sep(4, color)
        labels.append(Sg.Text(f"Tiempo: {time}", k='-time-', font='Any 10',
                              background_color=color))
        content = list(reduce(lambda x, y: x + y, zip(labels, sep)))
        return self.frame("", content, color=color, x=True)

    def replied(self, answers):
        labels = [self.labels(
            [f"{i + 1}: |" if resp is None else f"{i + 1}: {resp}|"])
            for i, resp in enumerate(answers)]
        return self.frame("Respuestas", reduce(lambda x, y: x + y, labels),
                          x=True)

    def clues(self, card, rounds, clues, opciones, opc_title):
        labels = [self.labels([f"{opc_title[i].capitalize()}:\n"
                               f"   {i + 1}. {clue}"])
                  for i, clue in enumerate(clues)]

        buttons = random.sample(self.buttons(opciones), len(opciones))
        return self.frame(f"{card}/{rounds}",
                          [self.column(labels + buttons)], x=True)

    def action(self) -> List[Sg.Frame]:
        return [Sg.Push()] + self.frame('', self.horizontal_bttns(
            ['Pasar', 'Abandonar']))


class ScreenProfiles(Interface):
    def __init__(self):
        super().__init__()

    def update_layout(self):
        buttons = self.horizontal_bttns(['Aceptar', 'Salir'])
        content = self.zip_labels_inputs(['Nick', 'Genero', 'Edad'], 3,
                                         ['-users-', '-genero-', '-edad-'])
        frame = self.frame('Nuevo Usuario', [self.column(content)])
        return self.menu([[Sg.VPush()], frame, buttons, [Sg.VPush()]])

    def screen(self):
        buttons = self.horizontal_bttns(['Guardar', 'Salir'])
        content = [[Sg.VPush()], [self.labels(['Usuario:'])[0], self.sep(1)[0],
                                  self.combo(list(self.data.users.keys()),
                                             '-seleccion-')]]
        content += self.zip_labels_inputs(['Genero:', 'Edad:'], 2,
                                          ['-genero-', '-edad-'])
        content.append([Sg.VPush()])
        column = self.column(content)
        frame = self.frame('Usuarios', [column], y=True)
        return self.menu([[Sg.VPush()], self.buttons(['Nuevo']),
                          [frame], buttons, [Sg.VPush()]])


class ScreenSettings(Interface):
    def __init__(self):
        super().__init__()
        self._labels = {'-name-': 'Nombre',
                        '-time-': 'Tiempo límite por ronda',
                        '-rounds-': 'Cantidad de rondas por juego',
                        '-correct-': 'Puntaje respuesta correcta',
                        '-incorrect-': 'Puntaje respuesta incorrecta',
                        '-clues-': 'Pistas a mostrar'}

    def screen(self):
        content = self.zip_labels_inputs(self._labels.values(), 6,
                                         self._labels.keys())
        niveles = self.frame('Niveles',
                             [self.combo(list(self.data.config.keys()),
                                         key='-list-')])
        edicion = self.frame('Edicion', [self.column(content, key='edit')],
                             y=True)
        accion = self.horizontal_bttns(['Guardar', 'Salir'])
        return self.menu([[self.column([niveles, edicion, accion])]])

    def get_label(self, key):
        return self._labels[key]


class ScreenScore(Interface):
    def __init__(self):
        super().__init__()

    def screen(self):
        niveles = self.frame('Niveles',
                             [self.combo(list(self.data.scores.keys()),
                                         key='-list-')])
        tablas = self.frame('Puntajes', [self.table(f"table-{i}",
                                                    ['Usuario',
                                                     'Puntajes'], [])
                                         for i in range(1, 3)], y=True)
        return self.menu([[niveles], [tablas], self.buttons(['Salir'])])


class Pop:

    @staticmethod
    def error(msj: str) -> bool:
        """ Emite un popup :arg msj: String con el mensaje a mostrar
        :arg msj: para casos de fracaso  o error"""
        Sg.popup(msj, no_titlebar=True, background_color="tomato")
        return False

    @staticmethod
    def ok(msj: str) -> None:
        """ Emite un popup :arg msj: String con el mensaje a mostrar
        :arg pantalla: para casos de exito"""
        Sg.popup(msj, no_titlebar=True, background_color="YellowGreen")
