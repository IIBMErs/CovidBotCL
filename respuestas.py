from covidsqlbase  import CovidDataBase
from parameters import PATH_LISTA_COMUNAS
import pandas as pd

class Respuesta:

    def __init__(self):
        self.covid_data_base = CovidDataBase

    @property
    def get_comunas(self):
        fileDir = PATH_LISTA_COMUNAS
        comunas = pd.read_csv(fileDir).Comuna.values
        
        comunas = [c for c in comunas if "Desconocido" not in c]
        return comunas
        

    def registro_response(self, user_id):
        # Comprobar que el usuario este en la base
        if self.user_in_base(user_id):
            # si esta registrado comprobar comunas
            with self.covid_data_base() as base:
                comunas = base.getUserComunas(user_id)

                if comunas == []: # Si no hay comunas
                    text = "Usted no ha registrado su comuna, por favor seleccióne Agregar Comuna para registrar una\. *Puede repetir este proceso para agregar varias\.*"

                else:
                    # si tiene comunas registradas
                    temp = ""
                    for comuna in comunas:
                        temp = temp + "*" + comuna[0] + "*" + ","
                    texto = "Usted se encuentra registrado en\: " + temp[:-2] +"\." + "\nPara agregar otra comuna seleccióne Agregar Comuna"
        else:
            text = "Usted no ha registrado su comuna, por favor seleccióne Agregar Comuna para registrar una\. *Puede repetir este proceso para agregar varias\.*"

        return text




    def user_in_base(self, user_id):
        with self.covid_data_base() as base:
            if (user_id,) in base.getUsers():
                return True      
            else:
                return False





