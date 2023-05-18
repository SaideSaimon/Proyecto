import json
import os.path
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


# Duración total de la partida (desde que el usuarie empieza a jugar)


class Analysis:
    def __init__(self):
        self.record = self.get_logs()
        self.partidas = self.get_partidas()
        self.users = self.get_users()

    # -----------------------Funciones Generales------------------------------

    @staticmethod
    def get_logs() -> pd.DataFrame:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '..', 'jsons', 'records.csv')
        return pd.read_csv(path, encoding="UTF-8")

    def get_partidas(self):
        """ Retorna una lista de partidas separadas por ID"""
        return [pd.DataFrame(self.record.loc[self.record['id'] == uid])
                for uid in self.record['id'].unique()]

    @staticmethod
    def get_users():
        path = os.path.join(os.getcwd(), '..', 'jsons', 'users.json')
        with open(path, 'r', encoding='UTF-8') as file:
            return json.load(file)

    def get_rows_cant(self, filtro: str, cond: str, *column):
        """ Retorna la cantidad de ocurrencias de una columna filtradas
        por una condición en la columna filtro \n
        column, estado -> 'timestamp', 'id', 'estado', 'usuario', 'evento'
         'texto ingresado', 'respuesta', 'nivel' \n
        cond -> 'ok', 'error', 'paso', 'inicio_partida', 'finalizada',
         'cancelada'"""
        logs = self.record
        return logs[list(column)].loc[logs[filtro] == cond]

    @staticmethod
    def calc_percent(valores):
        total = sum(valores)
        return map(lambda x: f"{x * 100 / total:.2f}%", valores)

    # ----------------------- Funciones Análisis -----------------------------

    # Top 10 de palabras que se encuentran primero de todas las partidas.
    def _top_teen_words(self):
        """ Retorna una lista [palabra, cantidad de veces adivinada primero]"""
        aciertos = self.get_rows_cant('estado', 'ok', 'texto ingresado',
                                      'id')
        apariciones = aciertos.groupby('id', sort=False).first()
        conteo = Counter(apariciones['texto ingresado']).most_common(10)
        return [[val[0], val[1]] for val in conteo]

    # Gráfico porcentaje partidas por estado
    def _percent_by_state(self):
        """ Porcentaje de partidas por estado """
        values = self.record.groupby(by=self.record['estado']).size()
        data = values.drop(['ok', 'paso'])
        labels = list(map(lambda x: x.capitalize(), data.keys()))
        fig, ax = plt.subplots()
        ax.pie(list(data), labels=labels,
               autopct=lambda val: f"{val:.2f}%")
        plt.show()

    # Gráfico que muestra el porcentaje de partidas finalizadas según género.
    def _percent_by_genere(self):
        """ Obtiene un frame con los usuarios que finalizaron las partidas
        y de cada uno el género para crear un gráfico con los porcentajes """
        ocurrencias = self.get_rows_cant('estado', 'finalizada', 'usuario')
        genere = pd.Series([self.users[user]['-genero-']
                            for user in ocurrencias['usuario']])
        genere = genere.value_counts()
        fig, ax = plt.subplots()
        ax.pie(genere.values, labels=genere.index,
               autopct=lambda val: f"{val:.2f}%", startangle=90)
        plt.show()

    # Gráfico que muestra el porcentaje de partidas finalizadas según nivel.
    def get_ended_games(self):
        niveles_cant = {'Facil': 0, 'Normal': 0, 'Dificil': 0, 'Custom': 0}
        niveles_fin = {'Facil': 0, 'Normal': 0, 'Dificil': 0, 'Custom': 0}
        x = self.get_partidas()
        for i in x:
            niveles_cant[i['nivel'].iloc[0]] += 1
            if i['estado'].iloc[-1] == 'finalizada':
                niveles_fin[i['nivel'].iloc[0]] += 1
        promedios = [float(niveles_fin[key] / val) for key, val in
                     niveles_cant.items() if val != 0]
        dificultades = ['Facil', 'Normal', 'Dificil', 'Custom']
        fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
        ax.bar(dificultades, promedios)
        plt.show()

    # Promedio de tiempo de respuesta para respuestas exitosas.
    @staticmethod
    def _time_of_ok_rounds(game) -> int:
        """ Retorna la suma de los tiempos en segundos que se tardó en dar
        una respuesta correcta, en caso de que no halla respuesta correcta
        en la partida retorna None"""
        t = [game['timestamp'][i] - game['timestamp'][i - 1]
             for i in game.index[1:] if game['estado'].loc[i] == 'ok']
        return sum(t) if t else None

    def _time_first_answer(self):
        """ Retorna del total de tiempos de respuesta exitosa, el promedio y
            el promedio de tiempo de todas las partidas"""
        tiempos_aciertos = pd.Series(map(self._time_of_ok_rounds,
                                         self.partidas))
        tiempos_aciertos.dropna(inplace=True)
        return f"Tiempo promedio aciertos: {tiempos_aciertos.mean():.2f}s"
    # ------------------------------

    # Promedio de tiempo de partida en general
    @staticmethod
    def _time_of(game):
        """ Retorna la duración de la partida (inicio_partida - fin)"""
        game.reset_index(drop=True, inplace=True)
        return game.iloc[-1, 0] - game.iloc[0, 0]

    def _time_general(self):
        tiempos_partida = pd.Series(map(self._time_of, self.partidas))
        return f"Tiempo promedio por partida: {tiempos_partida.mean():.2f}s"
    # ---------------------------------

    # Porcentaje de aciertos por usuario
    def _percent_by_users(self):
        users = list(self.users.keys())
        users.sort()
        rows = self.get_rows_cant('estado', 'ok', 'usuario').value_counts()
        index_l = [key[0] for key in rows.index]
        index_l.sort()
        percents = [[rows.index[i][0], val]
                    for i, val in enumerate(self.calc_percent(rows.values))]
        return percents if users == index_l \
            else percents + [[user, "0%"]
                             for user in set(index_l) ^ set(users)]

    # Cantidad de tarjetas para las que el usuario no dió respuesta (timeout).
    def _no_answer(self):
        tiempo = self.record['estado'] == 'timeout'
        return len(tiempo)

    # Cantidad de tarjetas en las que el usuario dió una respuesta errónea.
    def _wrong_answer(self):
        incorrectas = self.record[(self.record['estado'] == 'error') |
                                  (self.record['estado'] == 'paso')]
        return len(incorrectas)

    # Tiempo de la respuesta exitosa más rápida.
    def _fastest_answer(self):
        return min([self.record['timestamp'].loc[i] -
                    self.record['timestamp'].loc[i - 1]
                    for i in self.record.index
                    if self.record['estado'].loc[i] == 'ok'])

    def main(self):

        print("Top 10 Palabras primero acertadas ")
        for row in self._top_teen_words():
            print(f"{row[0]} {row[1]}")

        print("Porcentaje de partidas por estado")
        self._percent_by_state()

        print("Porcentaje de partidas finalizadas por genero")
        self._percent_by_genere()

        print("Porcentaje de partidas finalizadas por nivel")
        self.get_ended_games()

        print('Tiempo de la respuesta exitosa más rápida.')
        print(self._fastest_answer())

        print('Promedio de tiempo de respuesta para respuestas exitosas.')
        print(self._time_first_answer())

        print('Promedio de tiempo de partida generales')
        print(self._time_general())

        print('Porcentaje de aciertos por usuarie.')
        for row in self._percent_by_users():
            print(f"{row[0]} {row[1]}")

        print('Cantidad de tarjetas para las que el usuario '
              'no dió respuesta (timeout)')
        print(self._no_answer())

        print('Cantidad de tarjetas en las que el usuario '
              'dió una respuesta errónea.')
        print(self._wrong_answer())

Analysis().main()