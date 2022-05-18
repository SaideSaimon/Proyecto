import PySimpleGUI as Sg


class Login:
    def __init__(self):
        """ creamos la interfaz de la ventana de creacion de perfil
        
            falta pensar y resolver como trabajar las actualizaciones """
        self._window = self.crear_pantalla()

        self.loop()
        pass

    def crear_pantalla(self):
        """
        Agrego input text para recoger información y
        los botones para aceptar y salir
        """
        nombre_login = "Login"
        layout = [[Sg.Text('Nombre Usuario', size=(10, 1)),
                   Sg.InputText(key="-user-")],
                  [Sg.Text('Genero auto percibido', size=(10, 1)),
                   Sg.InputText(key='-genero-')],
                  [Sg.Text('edad', size=(10, 1)), Sg.InputText(key='-edad-')],
                  [Sg.Button('Aceptar', key="-ok-", size=(12, 2)),
                   Sg.Button('Salir', key="-Exit-", size=(12, 2))]]
        ventana_login = Sg.Window(nombre_login, layout, size=(500, 400),
                                  finalize=True)
        return ventana_login

    def loop(self):
        """Acá capturamos el evento del login"""

        while True:
            event, values = self._window.read()
            print(f"Ventana actual:  Evento: {event}, valores: {values}")

            if event == Sg.WIN_CLOSED or event == "-Exit-":
                break

        self._window.close()
