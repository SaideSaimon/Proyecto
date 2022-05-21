import json
import os.path
import PySimpleGUI as Sg

path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    "config.json")


def get_settings():
    with open(path, "r", encoding="UTF-8") as config:
        return json.load(config)


def set_settings(new_config):
    with open(path, "w", encoding="UTF-8") as file:
        json.dump(new_config, file, indent=4)
    Sg.Popup("Guardado", no_titlebar=True,background_color="DarkGrey",
             auto_close=True, auto_close_duration=2)
