import os.path
from os import walk


class FilesGetter:
    def __init__(self):
        self._local = os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def get_files(file_type: str, path_folder: str) -> list:
        """ Retorna todos los archivos que coinciden con 'file_type'
        en la carpeta 'path_folder' en una lista
        :param file_type: Tipo de archivo a buscar
        :param path_folder: Ruta al directorio """
        return list(filter(lambda file: file_type in file,
                           next(walk(path_folder), (None, None, []))[2]))

    @staticmethod
    def get_paths(path, files) -> list:
        """ Retorna una lista de rutas """
        return list(map(lambda file: os.path.join(path, file), files))

    def get_directory(self, file_type: str, folder: str) -> dict:
        """ Dada una carpeta y un tipo de archivo retorna un diccionario \n
        'nombre del archivo': ruta del archivo """
        path_folder = os.path.join(self._local, '..', '..', folder)
        keys = self.get_files(file_type, path_folder)
        paths = {keys[i][:keys[i].index('.')]: path
                 for i, path in enumerate(self.get_paths(path_folder, keys))}
        paths['root'] = path_folder
        return paths

