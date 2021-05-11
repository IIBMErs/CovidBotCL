import pandas as pd
from parameters import PATH_FASES

class Fase:
    def __init__(self):
        self.dir  = PATH_FASES
        self.data  = pd.read_csv(self.dir) 

        self.get_fases()


    def get_fases(self):
        last_date =self.data.columns.values[-1]
        dict_fases = {}
        for comuna in self.data["comuna_residencia"]:
            comuna_index = self.data[self.data["comuna_residencia"] == comuna]

            fase = comuna_index[last_date].values[0]
            comuna = comuna.replace('ñ','n')
            comuna = comuna.replace('ü','u')
            # Reemplazar acentos
            comuna = comuna.replace('á','a')
            comuna = comuna.replace('é','e')
            comuna = comuna.replace('í','i')
            comuna = comuna.replace('ó','o')
            comuna = comuna.replace('ú','u')
          

            comuna = comuna.replace('Ñ','N')
            comuna = comuna.replace('Á','A')

            dict_fases[comuna] = fase

        self.dict_fases = dict_fases

    def fase_de_comuna(self, comuna):
        return self.dict_fases[comuna]


if __name__ == "__main__":
    from time import time

    fase = Fase()

    t =time()
    print(fase.fase_de_comuna("Camina"))
    print(time()- t)
