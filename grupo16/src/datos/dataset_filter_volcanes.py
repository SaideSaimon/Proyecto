import csv
import os


def crear(lista, cambio):
    cabecera = ('Year', 'Volcanic Explosivity Index', 'Volcano Type',
                'Flag Tsunami', 'Flag Earthquake', 'Name and country')
    cambio.writerow(cabecera)
    for i in lista:
        cambio.writerow(i)


def cambiar(contenido):
    listado = []
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
                    'Maar':  'Maar',
                    'Subglacial volcano': 'Volcán subglacial',
                    'Compound volcano': 'Volcán compuesto',
                    'Submarine volcanoes': 'Volcanes submarinos',
                    'Volcanic field': 'Campo volcánico',
                    'Submarine volcano': 'Volcán submarino',
                    'Lava dome': 'Domo de lava',
                    'Mud volcano':  'Volcán de lodo',
                    'Crater rows':  'Hileras de cráteres',
                    'Shield volcano':  'Volcán escudo'}
    next(contenido)
    for data in contenido:
        nombre = data[5] + '(' + data[7] + ')'
        aux = [data[0], data[11], volcanes_ing[data[9]],
               True if data[3] == '' else False,
               True if data[4] == '' else False, nombre]
        listado.append(aux)
    return listado


def main():
    dir_of = os.path.join(os.getcwd(), 'datasets')
    arch_path = os.path.join(dir_of, 'volcanic-database.csv')
    arch_path2 = os.path.join(dir_of, 'volcanes_filtrado.csv')
    with open(arch_path, 'r', encoding='utf-8') as archivo:
        contenido = csv.reader(archivo, delimiter=';')
        cambio = cambiar(contenido)
    with open(arch_path2, 'w', encoding='utf-8') as cambiado:
        nuevo_cont = csv.writer(cambiado, lineterminator="\n")
        crear(cambio, nuevo_cont)


if __name__ == '__main__':
    main()
