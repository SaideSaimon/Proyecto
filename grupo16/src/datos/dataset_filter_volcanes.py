import pandas as pd
from Paths import GetPath
from typing import List


def unir(row: pd.read_csv) -> str:
    return row["Volcano Name"] + '(' + row["Country"] + ')'


def traducir(row: pd.read_csv) -> str:
    volcanes_ing = {'Pyroclastic shield': 'Escudo piroclástico',
                    'Caldera': 'Caldera',
                    'Complex volcano': 'Volcán complejo',
                    'Lava cone': 'Cono de lava',
                    'Cinder cone': 'Cono de ceniza',
                    'Tuff cone': 'Cono de toba',
                    'Stratovolcano': 'Estratovolcán',
                    'Pyroclastic cone': 'Cono piroclástico',
                    'Fissure vent': 'Respiradero de fisura',
                    'Pumice cone': 'Cono de piedra pómez',
                    'Maar': 'Maar',
                    'Subglacial volcano': 'Volcán subglacial',
                    'Compound volcano': 'Volcán compuesto',
                    'Submarine volcanoes': 'Volcanes submarinos',
                    'Volcanic field': 'Campo volcánico',
                    'Submarine volcano': 'Volcán submarino',
                    'Lava dome': 'Domo de lava',
                    'Mud volcano': 'Volcán de lodo',
                    'Crater rows': 'Hileras de cráteres',
                    'Shield volcano': 'Volcán escudo'}
    return volcanes_ing[row['Volcano Type']]


def transformar(row: pd.read_csv) -> bool:
    return False if row != '' else True


def cambiar(contenido: pd.read_csv) -> List[List[str | bool | str]]:
    cabecera = ['Year', 'Volcanic Explosivity Index', 'Volcano Type',
                'Flag Tsunami', 'Flag Earthquake', 'Name and Country']
    contenido["Name and Country"] = contenido.apply(unir, axis=1)
    contenido['Traduccion'] = contenido.apply(traducir, axis=1)
    contenido.drop(columns=['Volcano Name', 'Country', 'Volcano Type'])
    contenido.rename(columns={'Traduccion': 'Volcano Type'})
    contenido['Flag Earthquake'] = contenido['Flag Earthquake'].\
        apply(transformar)
    contenido['Flag Tsunami'] = contenido['Flag Tsunami'].apply(transformar)
    contenido = contenido.drop(columns=['Volcano Name', 'Country', 'Volcano '
                                                                   'Type']). \
        rename(columns={'Traduccion': 'Volcano Type'})
    return contenido[cabecera]


def main() -> None:
    path = GetPath().read_file('volcanes')
    file = pd.read_csv(path, delimiter=';')
    new_file = cambiar(file)
    new_file.to_csv(GetPath().write_file('volcanes'), index=False)


if __name__ == '__main__':
    main()
