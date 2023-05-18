import os.path
import PySimpleGUI as Sg
from src.template.utilitis.DAO import JsonsFiles
from typing import List, Dict


class Settings:
    def __init__(self):
        self._config = JsonsFiles().get_json('config')
        self._labels = {'-name-': 'Nombre',
                        '-time-': 'Tiempo límite por ronda',
                        '-rounds-': 'Cantidad de rondas por juego',
                        '-correct-': 'Puntaje respuesta correcta',
                        '-incorrect-': 'Puntaje respuesta incorrecta',
                        '-clues-': 'Pistas a mostrar'}
        self._window = self.make_window()

    @staticmethod
    def popup_bad(msj: str) -> None:
        """ Emite un popup :arg msj: String con el mensaje a mostrar
        :arg pantalla: para casos de fracaso  o error"""
        Sg.popup(msj, no_titlebar=True, background_color="tomato")

    @staticmethod
    def get_input_text(frame_values: List[str]) -> List[str]:
        """ Retorna la caja del input"""
        return [box[2] for i, box in enumerate(frame_values.Rows)]

    def set_values_input(self, frame_values: List[str], items: List[str]) -> \
            None:
        """
        Modifica los valores de los inputs con los valores que están en el json
        """
        content = list(zip(self.get_input_text(frame_values), items))
        for element, item in content:
            element.update(value=item)

    @staticmethod
    def update_list(window: Sg.Window, config_json: Dict[str, int]) -> None:
        """Actualiza los valores de la lista"""
        window.find_element("-list-").update(values=list(config_json.keys()))

    def verificar(self, values: Dict[str, int]) -> bool:
        """ Verifica que los inputs tengan valores correctos """
        values.pop('-list-')
        val = values.pop('-name-')
        if val in ("Easy", "Normal", "Hard"):
            self.popup_bad("Nivel no editable")
            return False
        elif val == 'Custom':
            for val, key in zip(values.values(), values.keys()):
                try:
                    values[key] = int(val)
                except ValueError:
                    self.popup_bad(f'Valor no valido "{val}" entrada: '
                                   f'{self._labels[key]}')
                    return False
        else:
            self.popup_bad('No se puede cambiar los nombres de los niveles'
                           if val != "" else "Elija un nivel para editar")
            return False
        return True

    def make_labels(self) -> List[Sg.Text]:
        """ Crea los textos a la izquierda del input """
        return [Sg.Text(label) for label in self._labels.values()]

    def make_inputs(self) -> List[Sg.InputText]:
        """ Crea los inputs """
        return [Sg.InputText(size=(10, 1), k=key, justification='right')
                for key in self._labels.keys()]

    def make_edition_frame(self, title: str) -> Sg.Frame:
        esp = [Sg.Push(), Sg.Push(), Sg.Push(),
               Sg.Push(), Sg.Push(), Sg.Push()]
        content = list(zip(self.make_labels(), esp, self.make_inputs()))
        column = Sg.Column([[label, space, input_text]
                            for label, space, input_text in content], k='edit')
        return Sg.Frame(title, [[column]], expand_x=True)

    @staticmethod
    def make_levels_frame(title: str, *args: List[str]) -> Sg.Frame:
        levels = Sg.Combo([key for key in args[0]],
                          key='-list-',
                          size=(40, 5),
                          enable_events=True)
        return Sg.Frame(title, [[levels]], k=f"-{title.lower()}-",
                        expand_x=True)

    @staticmethod
    def make_action_frame(title: str) -> Sg.Frame:
        buttons = [[Sg.Push(), Sg.Button('Guardar', key="-save-", size=(12, 1),
                                         border_width=0),
                    Sg.Button('Salir', key="-done-", size=(12, 1),
                              border_width=0)]]
        return Sg.Frame("", buttons, k=f"-{title.lower()}-", border_width=0,
                        expand_x=True)

    def make_window(self) -> Sg.Window:
        """
        Crea ventana con tres frames:
        edición, lista actual de niveles y botones de acción.
        """
        layout = [[Sg.Column([[self.make_levels_frame('Niveles',
                                                      self._config.keys())]])],
                  [Sg.Column([[self.make_edition_frame('Edición')]])],
                  [self.make_action_frame('Acciones')]]
        return Sg.Window("Configuración", layout, size=(400, 330),
                         element_justification='center',
                         titlebar_background_color='#f1d6ab',
                         titlebar_text_color='#38470b',
                         titlebar_icon=os.path.join(os.getcwd(), "icon.png"),
                         finalize=True)

    def loop(self) -> None:
        while True:
            event, values = self._window.read()
            print("evento: ", event, "valor: ", values)
            match event:
                case Sg.WIN_CLOSED | "-done-":
                    break
                case '-list-':
                    name = values['-list-']
                    items = [name] + list(self._config[name].values())
                    self.set_values_input(self._window.find_element('edit'),
                                          items)
                case '-save-':
                    if self.verificar(values):
                        self._config['Custom'] = values
                        JsonsFiles().set_json('config', self._config)

        self._window.close()
