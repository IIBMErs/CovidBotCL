
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib
import time
from tqdm import tqdm
from abc import ABC, abstractmethod
from parameters import PATH_CASOS_DIARIOS, PATH_CASOS_INCREMENTALES

class Data(ABC):

    def __init__(self,nombre_dato, ruta_archivo):
        self.data = pd.read_csv(ruta_archivo)
        self.weeks = 8  # Cantidad de semanas para hacer los datos
        self.nombre_dato = nombre_dato

    @property
    def dates(self):
        return [fecha for fecha in self.data.columns.values if '-' in fecha]

    def fechas_ultimas_semanas(self):
        # Entrega los puntos que se encuentran dentro de las ultimas self.weeks semanas
        reciente = datetime.strptime(self.dates[-1], "%Y-%m-%d")
        
        wanted_dates = []
        for fecha in self.dates[::-1]:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            if (reciente - fecha_obj).days <= self.weeks*7:
                wanted_dates.append(fecha)
        wanted_dates.reverse()

        return wanted_dates

    @property
    def comunas(self):
        comunas = self.data['Comuna'].values
        comunas = [c for c in comunas if "Desconocido" not in c and "Total" not in c]
        return comunas

    def plot(self, comuna, test=False):
        x,y = self.puntos(comuna)

        plt.plot_date(x,y,linestyle='-')
        plt.xticks(rotation=90)
        plt.title(f'Casos Diarios en {comuna}, {self.weeks} ultimas semanas')

        if test:
            plt.show()

        if not test:
            plt.savefig(f"images/{self.nombre_dato}-{comuna}-weeks{self.weeks}.png")
            plt.close()
            print(1)

    def test_plot(self):
        self.plot('Macul', test=True)

    def generar_plots(self):
        for comuna in tqdm(self.comunas):
            self.plot(comuna)
    
    @abstractmethod
    def puntos(self, comuna):
        comuna_data = self.data[self.data["Comuna"] == comuna]
        x = self.fechas_ultimas_semanas()
        y = comuna_data[x].values[0]
        return (x, y)




class CasosIncrementales(Data):

    def __init__(self, nombre_data, ruta_archivo):
        super().__init__(nombre_data, ruta_archivo)

    def puntos(self, comuna):
        return super().puntos(comuna)


class CasosDiarios(Data):
    
    def __init__(self, nombre_data, ruta_archivo):
        super().__init__(nombre_data, ruta_archivo)

    def puntos(self, comuna):
        return super().puntos(comuna)
    


def todos_los_datos():
    lista_datos = [
        CasosDiarios("casosDiarios", PATH_CASOS_DIARIOS),
        CasosIncrementales("casosIncrementales", PATH_CASOS_INCREMENTALES)
    ]

    for dato in lista_datos:
        dato.generar_plots()

if __name__ == "__main__":
    from parameters import PATH_CASOS_DIARIOS, PATH_CASOS_INCREMENTALES
    test = CasosIncrementales("casosDiarios", PATH_CASOS_INCREMENTALES)

    todos_los_datos()