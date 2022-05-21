import PySimpleGUI as Sg
from ..datos.manejador_json import set_settings, get_settings


class Settings:
    def __init__(self):
        self._config = get_settings()
        self._window = self.make_window()
        self._errors = Errors()
        self.loop()

    def make_labels(self):
        """ Crea los textos a la izquierda del input """
        items = ['Nombre', 'Tiempo límite por ronda',
                 'Cantidad de rondas por juego',
                 'Puntaje sumado por cada respuesta correcta',
                 'Puntaje sumado por cada respuesta incorrecta',
                 'Cantidad de características a mostrar']
        return [Sg.Text(label) for label in items]

    def make_inputs(self):
        """ Crea los inputs """
        keys = ['-name-', '-time-', '-rounds-',
                '-correct-', '-incorrect-', '-clues-']
        return [Sg.InputText(size=(10, 1), readonly=False, k=key)
                for key in keys]

    def get_input_text(self, frame_values):
        """ Retorna la caja del input"""
        return [box[1] for i, box in enumerate(frame_values.Rows)]

    def set_values_input(self, frame_values, items):
        """
        Modifica los valores de los inputs con los valores que están en el json
        """
        content = list(zip(self.get_input_text(frame_values), items))
        for element, item in content:
            element.update(value=item)


    def update_list(self, window, config_json):
        """Actualiza los valores de la lista"""
        window.find_element("-list-").update(values=list(config_json.keys()))

    def make_edition_frame(self, title):
        content = list(zip(self.make_labels(), self.make_inputs()))
        column = Sg.Column([[label, input_text]
                            for label, input_text in content])
        return Sg.Frame(title, [[column]], k=title, expand_x=True)

    def make_levels_frame(self, title, *args):
        levels = Sg.Listbox([key for key in args[0]],
                            key='-list-',
                            size=(40, 5),
                            enable_events=True)
        return Sg.Frame(title, [[levels]], k=title, expand_x=True)

    def make_accion_frame(self, title):
        buttons = [[Sg.Button('Guardar', key="-save-", size=(12, 1)),
                    Sg.Button('Eliminar', key="-delete-", size=(12, 1)),
                    Sg.Button('Salir', key="-done-", size=(12, 1))]]
        return Sg.Frame(title, buttons, k=title, expand_x=True)

    def make_window(self):
        """
        :return: ventana con tres frames: edición, lista actual de niveles y botones de acción.
        """
        title = "Settings"
        layout = [[Sg.Column([[self.make_edition_frame('Edición')]])],
                  [Sg.Column([[self.make_levels_frame('Niveles',
                                                      self._config.keys())]])],
                  [self.make_accion_frame('Acciones')]]
        return Sg.Window(title, layout, size=(500, 400), finalize=True)

    def loop(self):

        while True:
            event, values = self._window.read()
            print("evento: ", event, "valor: ", values)
            match event:
                case Sg.WIN_CLOSED | "-done-":
                    break
                case '-list-':
                    name = values['-list-'].pop()
                    items = [name] + list(self._config[name].values())
                    self.set_values_input(self._window.element_list()[2],
                                          items)
                case '-save-':
                    try:
                        name = values.pop('-list-')[0]
                    except IndexError:
                        self._errors.index_error()
                    else:
                        if name == 'custom':
                            text_input = list(zip(values.values(),
                                                  values.keys()))[1:]
                            save = True
                            for val, key in text_input:
                                try:
                                    values[key] = int(val)
                                except ValueError:
                                    self._errors.value_error(val, key)
                                    save = False
                                    break
                            if save:
                                self._config[values.pop('-name-')] = values
                                set_settings(self._config)
                                self.update_list(self._window, self._config)
                        else:
                            self._errors.no_editable(name)
                case '-delete-':
                    try:
                        name = values.pop('-list-')[0]
                    except IndexError:
                        self._errors.index_error()
                    else:
                        if name == 'custom':
                            self._config.__delitem__(values['-list-'].pop())
                            self.update_list(self._window, self._config)
                            self.set_values_input(self._window.element_list()[2],
                                                  ["" for x in range(6)])
                            set_settings(self._config)
                        else:
                            self._errors.no_editable(name)

        self._window.close()

class Errors:

    def get_label(self, key):
        if key == '-name-':
            return 'Nombre'
        elif key == '-time-':
            return 'Tiempo límite por ronda'
        elif key == '-rounds-':
            return 'Cantidad de rondas por juego'
        elif key == '-correct-':
            return 'Puntaje sumado por cada respuesta correcta'
        elif key == '-incorrect-':
            return 'Puntaje sumado por cada respuesta incorrecta'
        else:
            return 'Cantidad de características a mostrar'

    def index_error(self):
        Sg.popup_auto_close("Elija nivel a editar",
                            auto_close_duration=2,
                            no_titlebar=True,
                            background_color="DarkGrey")

    def value_error(self, val, key):
        Sg.popup_auto_close(f'Valor no valido '
                            f'" {val} "'
                            f'input: {self.get_label(key)}',
                            auto_close_duration=2,
                            no_titlebar=True,
                            background_color="DarkGrey")

    def no_editable(self, name):
        Sg.popup_auto_close(f'Nivel "{name}" no editable ',
                            auto_close_duration=2,
                            no_titlebar=True,
                            background_color="DarkGrey")
