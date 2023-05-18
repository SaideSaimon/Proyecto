import os

from src.template.pantalla_menu import MainMenu


class Main:
    def __init__(self):

        self._window = MainMenu().loop()


Main()
