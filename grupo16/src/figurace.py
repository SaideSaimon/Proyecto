import PySimpleGUI as sg
from template.pantalla_menu import MainMenu
class Main():
    """  la clase Main  es la entrada a la aplicacion
         """

    def __init__(self):
        """
        creamos la ventana del menu principal y arranca la aplicacion 
        """
        self._window = MainMenu()
        pass


   

if __name__  == "__main__":
    main = Main()
    #main._window.loop()