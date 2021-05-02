import pandas as pd
from parameters import PATH_FASES

class Fase:
    def __init__(self):
        self.dir  = PATH_FASES
        self.data  = pd.read_csv(self.dir)


    def faseDeComuna(self,comuna):
        last_date =self.data.columns.values[-1]
        comuna_index = self.data[self.data["comuna_residencia"]==comuna]
        return comuna_index[last_date].values[0] # fase de la comuna
        




