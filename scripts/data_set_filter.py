import csv
import os.path
import re


def dms_dd(*args):
    """ Convertir de grados,minutos,segundos a decimal"""
    def convert(dd):
        coord = int(dd[0]) + (float(dd[1]) / 60) + (float(dd[2]) / 60 ** 2)
        if dd[-1:][0] in ("E", "S"):
            coord *= -1
        return coord

    cords = "".join([","+convert(re.split(r"\W", dms)).__format__(".4")
                     for dms in args])
    return cords[1:]


def get_content():
    """
    "Ubicación", "Superficie (km²)", “Profundidad
    máxima (m)”, “Profundidad media (m)”, "Coordenadas"
    """
    file_read = "Lagos Argentina - Hoja 1.csv"
    file_write = "Lagos_Argentina.csv "
    path_read = os.path.join(os.getcwd(), file_read)
    path_write = os.path.join(os.getcwd(), file_write)

    with open(path_read, 'r', encoding="UTF-8") as file_r:
        file_reader = csv.reader(file_r)
        with open(path_write, "w", encoding="UTF-8") as file_w:
            file_writer = csv.writer(file_w)
            file_writer.writerow(next(file_reader))
            for line in file_reader:
                x, y = line[-1:][0].split()
                line[-1] = dms_dd(x, y)
                file_writer.writerow(line)


if __name__ == '__main__':
    get_content()
