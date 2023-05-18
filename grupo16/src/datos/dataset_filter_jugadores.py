from Paths import GetPath
import pandas as pd

positions = {"GK": "Portero",
             "RWB": "Carrilero Derecho",
             "RB": "Lateral Derecho",
             "CB": "Defensa Central",
             "LB": "Lateral Izquierdo",
             "LWB": "Carrilero Izquierdo",
             "CDM": "Medio Centro Defensivo",
             "RM": "Medio Derecho",
             "CM": "Medio Centro",
             "LM": "Medio Izquierdo",
             "CAM": "Medio Centro Ofensivo",
             "RF": "Segundo Delantero Derecho",
             "CF": "Media Punta",
             "LF": "Segundo Delantero Izquierdo",
             "RW": "Extremo Derecho",
             "ST": "Delantero Centro",
             "LW": "Extremo Izquierdo"}


def get_position(pos: str) -> str:
    return positions[pos] if "|" not in pos \
        else "".join([positions[i] + " | " for i in pos.split("|")])[:-3]


def get_potential(potencial: int) -> str:
    if potencial <= 60:
        return "Regular"
    elif potencial <= 79:
        return "Bueno"
    elif potencial <= 89:
        return "Muy Bueno"
    else:
        return "Sobresaliente"


def filtrar_linea(team: str, country: str, position: str, age: str,
                  potential: str, name: str) -> list:
    """ Recibe por parámetro cada uno de los elementos que contienen
    la fila y los procesa por separado retornando una lista"""
    return [team[:-1], country, get_position(position),
            age, get_potential(int(potential)), name]


def get_file(file, headers):
    return pd.DataFrame(map(lambda line: filtrar_linea(*line),
                            file.values), columns=headers)


def main() -> None:
    headers = ["team", "nationality", "position", "age", "potential", "name"]
    path = GetPath().read_file('fifa')
    if path:
        file = get_file(pd.read_csv(path, delimiter=';')[headers], headers)
        file.to_csv(GetPath().write_file('fifa'), index=False)


main()
