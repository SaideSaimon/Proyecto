import csv
import os.path
import re


def convert(grade, minute, second, orientation):
    position = int(grade) + float(minute) / 60 + float(second) / 3600
    return position if orientation not in ("O", "S") else position * -1


def get_decimal_degrees(values):
    """ Convierte de grados,minutos,segundos a grados decimal"""
    return ''.join(["," + convert(*re.split("[°'\"]", dms)).__format__(".4")
                    for dms in values.split()])[1:]


def comb_for_the(line):
    """
    Convierte a grados decimales cada elemento de la última columna y
    pasa la primera columna al final
    """
    line.append(get_decimal_degrees(line.pop()))
    line.append(line.pop(0))
    return line


def make_file():
    """
    Crea un archivo de texto del tipo csv con los preconceptos
    de la consigna dada.
    """

    dir_of = os.path.join(os.getcwd(), 'datasets')
    read_path = os.path.join(dir_of, "Lagos Argentina - Hoja 1.csv")
    writer_path = os.path.join(dir_of, "Lagos_Argentina_fltrado.csv")
    with open(read_path, 'r', encoding="UTF-8") as file_r:
        reader = csv.reader(file_r)
        with open(writer_path, "w", encoding="UTF-8") as file_w:
            writer = csv.writer(file_w, lineterminator="\n")
            headers = next(reader)
            headers.append(headers.pop(0))
            writer.writerow(headers)
            writer.writerows(list(map(comb_for_the, reader)))


if __name__ == '__main__':
    make_file()
