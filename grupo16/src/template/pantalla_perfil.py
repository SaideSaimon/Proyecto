import os
from typing import List, Dict
import PySimpleGUI as Sg
from src.template.utilitis.DAO import JsonsFiles


class Profiles:
    def __init__(self):
        self._user = JsonsFiles().get_json('users')
        self._pantalla_actual = None
        self._window = self.pantalla_eleccion()


    @staticmethod
    def popup_bad(msj: str) -> None:
        """ Emite un popup :arg msj: String con el mensaje a mostrar
        :arg pantalla: para casos de fracaso  o error"""
        Sg.popup(msj, no_titlebar=True, background_color="tomato")

    @staticmethod
    def popup_ok(msj: str) -> None:
        """ Emite un popup :arg msj: String con el mensaje a mostrar
        :arg pantalla: para casos de exito"""
        Sg.popup(msj, no_titlebar=True, background_color="YellowGreen")

    def verificar(self, values: Dict[str, str]) -> bool:
        """ Verifica que los inputs tengan valores correctos """
        for val, key in zip(values.values(), values.keys()):
            match key:
                case '-seleccion-':
                    if val not in self._user.keys():
                        self.popup_bad('Seleccione un usuario')
                        return False
                case '-genero-' | '-usuario-':
                    if key == '-usuario-' and val in self._user:
                        self.popup_bad('Usuario existente')
                        return False
                    if not val.isalpha():
                        self.popup_bad(f'Entrada "{key[1:-1]}", '
                                       f'valor no valido: "{val}"')
                        return False
                case '-edad-':
                    if not val.isdigit():
                        self.popup_bad(f'Entrada "{key[1:-1]}", '
                                       f'valor no valido: "{val}"')

                        return False
        return True

    @staticmethod
    def make_combo(values: Dict[str, str]) -> Sg.Combo:
        """ Crea la lista de los perfiles que existen """

        valores = list(values)
        return Sg.Combo(values=valores, readonly=True, enable_events=True,
                        k="-seleccion-", expand_x=True)

    def make_frame(self) -> List[Sg.Frame]:
        """Crea el frame con el combo y el editor de usuarios"""
        return [Sg.Frame("Usuarios", [[self.make_combo(self._user.keys())],
                                      [Sg.Text('Genero: ', size=(15, 1))],
                                      [Sg.InputText(key="-genero-")],
                                      [Sg.Text('Edad:', size=(15, 1))],
                                      [Sg.InputText(key="-edad-")]
                                      ],
                         expand_x=True, expand_y=True)]

    @staticmethod
    def pantalla_crear() -> Sg.Window:
        """ Pantalla para la creación de perfiles"""
        layout = [[Sg.Text('Nombre de usuario:', size=(25, 1))],
                  [Sg.Push(), Sg.InputText(key="-usuario-", size=(15, 1))],
                  [Sg.Text('Genero: ', size=(25, 1))],
                  [Sg.Push(), Sg.InputText(key="-genero-", size=(15, 1))],
                  [Sg.Text('Edad:', size=(25, 1))],
                  [Sg.Push(), Sg.InputText(key="-edad-", size=(15, 1))],
                  [Sg.Button('Aceptar', key='-Accept-', size=(10, 1),
                             border_width=0),
                   Sg.Button('Salir', key='-Exit-', size=(10, 1),
                             border_width=0)]]
        return Sg.Window("Crear Jugador", layout, size=(250, 250),
                         margins=(0, 15), titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         finalize=True)

    def pantalla_editar(self) -> Sg.Window:
        """ Pantalla para la edición de perfiles existentes"""
        layout = [self.make_frame(),
                  [Sg.Button('Aceptar', key='-Accept-', border_width=0,
                             size=(15, 1)),
                   Sg.Button('Salir', key='-Exit-', border_width=0,
                             size=(15, 1))]
                  ]
        return Sg.Window("Editar Jugador", layout, size=(250, 250),
                         titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         finalize=True)

    @staticmethod
    def pantalla_eleccion() -> Sg.Window:
        """Crea la pantalla con opciones para crear o editar un perfil"""
        principal = Sg.Column([[Sg.Button('Crear perfil', key="-Create-",
                                          size=(10, 1), border_width=0)],
                               [Sg.Button('Editar perfil', key="-Edit-",
                                          size=(10, 1), border_width=0)],
                               [Sg.Button('Salir', key="-Exit-",
                                          size=(10, 1), border_width=0)]],
                              justification='c')
        return Sg.Window("", [[Sg.Push(), principal, Sg.Push()]],
                         size=(250, 250),
                         titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         finalize=True)

    def loop_pantalla_crear(self) -> None:
        """Inicia el loop de la lectura de los eventos de la pantalla creación
        de perfiles"""
        pantalla = self.pantalla_crear()
        while True:
            event, values = pantalla.read()
            match event:
                case "-Accept-":
                    if self.verificar(values):
                        self._user[values.pop("-usuario-")] = values
                        JsonsFiles().set_json('users', self._user)
                        self.popup_ok(f'Nuevo usuario cargado.')
                        break

                case Sg.WIN_CLOSED | "-Exit-":
                    break
        pantalla.close()

    def loop_pantalla_editar(self) -> None:
        """Inicia el loop de la lectura de los eventos de la pantalla edición
        de perfiles"""
        pantalla = self.pantalla_editar()

        while True:
            event, values = pantalla.read()
            match event:
                case "-Accept-":
                    if self.verificar(values):
                        self._user[values.pop("-seleccion-")] = values
                        self.popup_ok(f'Nuevo usuario cargado correctamente.')
                        JsonsFiles().set_json('users', self._user)
                        break
                case "-seleccion-":
                    usuario = self._user[values["-seleccion-"]]
                    genero = pantalla.find_element("-genero-")
                    genero.update(value=usuario["-genero-"])
                    edad = pantalla.find_element("-edad-")
                    edad.update(value=usuario["-edad-"])
                case Sg.WIN_CLOSED | "-Exit-":
                    break
        pantalla.close()

    def loop(self) -> None:
        """ Inicia el loop de la lectura de los eventos de la pantalla """
        while True:
            event, values = self._window.read()
            match event:
                case "-Edit-":
                    self._window.hide()
                    self.loop_pantalla_editar()
                    self._window.un_hide()
                case "-Create-":
                    self._window.hide()
                    self.loop_pantalla_crear()
                    self._window.un_hide()
                case Sg.WIN_CLOSED | "-Exit-":
                    break
        self._window.close()
