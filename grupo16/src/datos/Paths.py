import os


class GetPath:
    def __init__(self):
        self._path = os.path.join(os.getcwd(), 'base')

    def read_file(self, file):
        files = list(filter(lambda file: 'csv' in file,
                            next(os.walk(self._path), (None, None, []))[2]))
        try:
            return os.path.join(self._path, files[files.index(file+'.csv')])
        except ValueError:
            return False

    def write_file(self, file):
        return os.path.join(self._path, '..', '..',
                            'datasets', f"filtrado_{file}.csv")
