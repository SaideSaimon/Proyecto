import re
from Paths import GetPath
import pandas as pd


def convert(grade: str, minute: str, second: str, orientation: str) -> float:
    position = int(grade) + float(minute) / 60 + float(second) / 3600
    return position if orientation not in ("O", "S") else position * -1


def get_decimal_degrees(values: str) -> str:
    """ Convierte de grados,minutos,segundos a grados decimal"""
    return ''.join(["," + convert(*re.split("[°'\"]", dms)).__format__(".4")
                    for dms in values.split()])[1:]


def make_file() -> None:
    """
    Crea un archivo csv con los preconceptos de la consigna dada.
    """
    path = GetPath().read_file('lagos')
    if path:
        file = pd.read_csv(path)
        headers = list(file.keys())
        headers.append(headers.pop(0))
        file = file.dropna()
        file['Coordenadas'] = file['Coordenadas'].apply(get_decimal_degrees)
        file = file[headers]
        file.to_csv(GetPath().write_file('lagos'), index=False)


if __name__ == '__main__':
    make_file()
