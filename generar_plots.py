import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import time
from tqdm import tqdm
from abc import ABC, abstractmethod
import parameters as p
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.io import write_image
from datetime import datetime
from fases import Fase
import locale
import json
locale.setlocale(locale.LC_TIME, '')


class Data(ABC):

    def __init__(self,nombre_dato, identificador, ruta_archivo):
        self.data = pd.read_csv(ruta_archivo)
        self.weeks = 32  # Cantidad de semanas para hacer los datos
        self.identificador = identificador
        self.nombre_dato = nombre_dato
        self.fase = Fase()

        self.leer_paso_a_paso()

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

    def leer_paso_a_paso(self):
        with open(p.PATH_PASO_A_PASO) as json_file:
            self.paso_a_paso = json.load(json_file)


    def plot(self, comuna, save=True):
        x, y = self.puntos(comuna) 
        plt.style.use('dark_background')

        try:
            self.fase.fase_de_comuna(comuna)
        except:
            print(comuna)
            return


        fig, (ax1, ax2, ax3) = plt.subplots(3,1, gridspec_kw={'height_ratios':[0.5,4,0.2]})
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

        ax2.plot_date(x,y,linestyle='-',color='y',mec='r')

        ax1.axis('off')
        ax3.axis('off')


        x_reverse = x[::-1]
        x_downsample = x_reverse[:-1:8][::-1]


        ax2.set_xticks(x_downsample)
        ax2.set_xticklabels(x_downsample)
        ax2.set_xlabel('Casos')
        ax2.grid()

        # Annotations
        plt.annotate(f"{self.nombre_dato} en {comuna}", xy=(0.1, 0.9),xycoords='figure fraction',fontsize=15)
        plt.annotate(f"Comuna en fase {self.fase.fase_de_comuna(comuna)}", xy=(0.1, 0.85),xycoords='figure fraction',fontsize=15)

        fig.savefig(f"images/{self.identificador}-{comuna}-weeks{self.weeks}.png")
        plt.close(fig)

    def test_plot(self):
        self.plot('Macul', save=False)

    def generar_plots(self):
        for comuna in tqdm(self.comunas):
            self.plot(comuna)
    
    @abstractmethod
    def puntos(self, comuna):
        comuna_data = self.data[self.data["Comuna"] == comuna]
        fechas = self.fechas_ultimas_semanas()
        casos = comuna_data[fechas].values[0]

        x = []
        y = []
        for i in range(len(fechas) - 1):
            fecha_inicial = datetime.strptime(fechas[i], "%Y-%m-%d")
            fecha_final = datetime.strptime(fechas[i + 1], "%Y-%m-%d")

            # Dias entre fechas
            dias = (fecha_final - fecha_inicial).days
            x.append(fechas[i + 1])
            y.append(casos[i + 1] / dias)
            
        #return fechas, casos
        return (x, y)




class CasosIncrementales(Data):

    def __init__(self, nombre_data, identificador, ruta_archivo):
        super().__init__(nombre_data, identificador, ruta_archivo)

    def puntos(self, comuna):
        return super().puntos(comuna)


class CasosDiarios(Data):
    
    def __init__(self, nombre_data, identificador, ruta_archivo):
        super().__init__(nombre_data, identificador, ruta_archivo)

    def puntos(self, comuna):
        return super().puntos(comuna)
    

class CasosActivos(Data):

    def __init__(self, nombre_data, identificador, ruta_archivo):
        super().__init__(nombre_data, identificador, ruta_archivo)

    def puntos(self, comuna):
        return super().puntos(comuna)

def generar_todos_los_plots():
    lista_datos = [
        CasosActivos("Casos Activos", "casosActivos", p.PATH_CASOS_ACTIVOS),
        CasosIncrementales("Casos Incrementales","casosIncrementales", p.PATH_CASOS_INCREMENTALES)
    ]

    for dato in lista_datos:
        dato.generar_plots()

if __name__ == "__main__":
    import os
    os.system('clear')
    test = CasosActivos("Casos Activos", "casosActivos", p.PATH_CASOS_ACTIVOS)
    #test.puntos("Macul")
    generar_todos_los_plots()