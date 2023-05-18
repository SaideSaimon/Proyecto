import os

import PySimpleGUI as Sg
from src.template.pantalla_jugar import Jugar
from src.template.pantalla_perfil import Profiles
from src.template.pantalla_configuracion import Settings
from src.template.pantalla_puntuacion import Puntuacion
from src.template.utilitis.DAO import JsonsFiles
from typing import List


class MainMenu:

    def __init__(self):
        self._levels, self._users = self.get_combo_values()
        self._puntaje = 0
        self._window = self.make_menu()

    @staticmethod
    def get_combo_values():
        js = JsonsFiles()
        return (list(js.get_json('config').keys()),
                list(js.get_json('users').keys()))

    @staticmethod
    def popup_bad(msj: str) -> None:
        """ Emite un popup con el mensaje a mostrar
        :arg msj: String"""
        Sg.popup(msj, no_titlebar=True, background_color="tomato")

    def update_users(self) -> None:
        """ Actualiza la lista de usuarios si se editó"""
        self._users = list(JsonsFiles().get_json('users').keys())

    # Preguntar
    @staticmethod
    def make_buttons() -> List[List[Sg.Button]]:
        """ Crea una lista de botones"""
        tittles = ["Jugar", "Perfiles", "Configuración", "Puntaje", "Salir"]
        return [[Sg.Button(title, k=f"-{title.lower()}-", border_width=0,
                           size=(20, 1))]
                for title in tittles]

    @staticmethod
    def make_combo(values: list, key: str) -> Sg.Combo:
        """ Crea la lista desplegable de usuarios o niveles \n
        :param values: Contenido del desplegable
        :param key: Clave asignada al Combo"""
        return Sg.Combo(values=values, readonly=True, enable_events=True,
                        k=key)

    def make_frame(self) -> List[List[Sg.Frame]]:
        """ Asigna al frame los dos combos de usuarios y niveles"""
        return [[Sg.Frame("  Dificultad      Usuario    ",
                          [[self.make_combo(self._levels, "-difficulty-"),
                            self.make_combo(self._users, "-user-")]])]]

    def make_menu(self) -> Sg.Window:
        """ Crea el menu de configuración"""
        Sg.theme_global('LightBrown11')
        layout = [[Sg.Column(self.make_buttons())], self.make_frame()]
        return Sg.Window("", layout, size=(250, 250),
                         element_justification='center',
                         titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         alpha_channel=1,
                         margins=(0, 15),
                         finalize=True)

    def loop(self) -> None:
        """ El loop permite leer los eventos de la pantalla y actuar
        basándose en el caso."""
        while True:
            event, values = self._window.read()
            print(f"event: {event}, values:{values} ")
            match event:
                case Sg.WIN_CLOSED | "-salir-":
                    break
                case "-jugar-":
                    level, user = list(values.values())
                    if level and user != '':
                        self._window.hide()
                        Jugar(level, user).loop()
                        self._window.un_hide()
                    else:
                        self.popup_bad("Elija un jugador o una dificultad")
                case "-perfiles-":
                    self._window.close()
                    Profiles().loop()
                    self.update_users()
                    self._window = self.make_menu()
                case "-configuración-":
                    self._window.hide()
                    Settings().loop()
                    self._window.un_hide()
                case "-puntaje-":
                    self._window.hide()
                    Puntuacion().loop()
                    self._window.un_hide()
        self._window.close()
