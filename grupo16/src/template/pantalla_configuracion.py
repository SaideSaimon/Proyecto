import json
import PySimpleGUI as Sg


class Settings:
    def __init__(self):
        self._window = make_window()
        self.loop()

    def loop(self):
        file_r = open('config.json', 'r')
        config_json = json.load(file_r)
        file_r.close()
        while True:
            event, values = self._window.read()
            print("evento: ",event, "valor: ", values)
            match event:
                case Sg.WIN_CLOSED | "-done-":
                    break
                case '-list-':
                    name = values['-list-'].pop()
                    items = [name] + list(config_json[name].values())
                    set_values_input(self._window.element_list()[2], items)
                case '-save-':
                    values.pop('-list-')
                    text_input = list(zip(values.values(), values.keys()))[1:]
                    for val, key in text_input:
                        try:
                            values[key] = int(val)
                        except ValueError:
                            Sg.popup_auto_close(f'Valor no valido '
                                                f'" {val} "input: {key[1:-1]}',
                                                auto_close_duration=2,
                                                no_titlebar=True,
                                                background_color="DarkGrey")

                            break
                    config_json[values.pop('-name-')] = values
                    with open('config.json', 'w') as file:
                        json.dump(config_json, file, indent=4)
                    update_list(self._window, config_json)
                case '-delete-':
                    config_json.__delitem__(values['-list-'].pop())
                    update_list(self._window, config_json)
                    set_values_input(self._window.element_list()[2],
                                     ["" for x in range(6)])
                    with open('config.json', 'w') as file:
                        json.dump(config_json, file, indent=4)

        self._window.close()


def make_labels():
    """ Crea los textos a la izquierda del input """
    items = ['Nombre', 'Tiempo límite por ronda',
             'Cantidad de rondas por juego',
             'Puntaje sumado por cada respuesta correcta',
             'Puntaje sumado por cada respuesta incorrecta',
             'Cantidad de características a mostrar']
    return [Sg.Text(label) for label in items]


def make_inputs():
    """ Crea los inputs """
    keys = ['-name-', '-time-', '-rounds-',
            '-correct-', '-incorrect-', '-clues-']
    return [Sg.InputText(size=(10, 1), k=key) for key in keys]


def get_input_text(frame_values):
    """ Retorna la caja del input"""
    return [box[1] for i, box in enumerate(frame_values.Rows)]


def set_values_input(frame_values, items):
    """
    Modifica los valores de los inputs con los valores que están en el json
    """
    for element, item in list(zip(get_input_text(frame_values), items)):
        element.update(value=item)


def update_list(window, config_json):
    """Actualiza los valores de la lista"""
    window.find_element("-list-").update(values=list(config_json.keys()))


def make_frame(title, *args):
    """
    :param title: "Edición" labels e inputs "Niveles" lista de niveles del json
    :param args: Usado para obtener las keys del json
    :return: frame con layouts
    """
    frame = Sg.Frame(title, [[]], k=title, expand_x=True)
    match title:
        case 'Edición':
            frame.layout(
                rows=[[Sg.Column([[label, input_text] for label, input_text in
                                  list(zip(make_labels(), make_inputs()))])]])
        case 'Niveles':
            frame.layout(
                rows=[[Sg.Column([[Sg.Listbox([key for key in args[0]],
                                              key='-list-',
                                              size=(40, 5),
                                              enable_events=True)]])]])
        case 'Acciones':
            frame.layout(
                rows=[[Sg.Button('Guardar', key="-save-", size=(12, 1)),
                       Sg.Button('Eliminar', key="-delete-", size=(12, 1)),
                       Sg.Button('Salir', key="-done-", size=(12, 1))]])
    return frame


def make_window():
    """
    :return: ventana con dos frames edición y lista actual de niveles
    """
    file_r = open('config.json', 'r', encoding="UTF-8")
    config = json.load(file_r)
    title = "Settings"
    layout = [[Sg.Column([[make_frame('Edición')]])],
              [Sg.Column([[make_frame('Niveles', config.keys())]])],
              [make_frame('Acciones')]]
    file_r.close()
    return Sg.Window(title, layout, size=(500, 400), finalize=True)
