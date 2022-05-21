import PySimpleGUI as Sg


class jugar():
    def __init__(self):
        """ creamos la interfaz de la ventana de jugar
                """
        self._window = self.crear_pantalla()

        self.loop()
        pass

    def crear_pantalla(self):
        """ agrego el boton terminar y salir que tendría
        que devolvernos al menu
            """
        nombre_juego = "Figurace"
        layout = [[Sg.Button("Salir", key="-Exit-", size=(10, 10))],
                  [Sg.Text('estamos jugando..', size=(30, 10))]
                  ]

        return Sg.Window(nombre_juego, layout, size=(500, 400),
                         finalize=True)

    def loop(self):
        """ aca se capturan todos los evenos que tenga nuestro juego
                """
        while True:
            event, values = self._window.read()
            print(f"Ventana actual:  Evento: {event}, valores: {values}")

            if event == Sg.WIN_CLOSED or event == "-Exit-":
                break
        self._window.close()
