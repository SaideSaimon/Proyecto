from src.template import *
from trabajo_integrador.grupo16.src.template import pantalla_menu


class Main:
    """
    La clase Main es la entrada a la aplicación
    """

    def __init__(self):
        """
        creamos la ventana del menu principal y arranca la aplicacion 
        """
        self._window = pantalla_menu.MainMenu()


Main()
