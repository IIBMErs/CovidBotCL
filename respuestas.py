from covidsqlbase  import CovidDataBase
from parameters import PATH_LISTA_COMUNAS, NOMBRE_BOT
import pandas as pd
from fases import Fase


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
                        temp = temp + "*" + comuna[0] + "*" + ", "
                    text = "Usted se encuentra registrado en\: " + temp[:-2] +"\." + "\nPara agregar otra comuna seleccióne Agregar Comuna"
        else:
            text = "Usted no ha registrado su comuna, por favor seleccióne Agregar Comuna para registrar una\. *Puede repetir este proceso para agregar varias\.*"

        
        return text

    
    def agregar_comuma_response(self, user_id, message, COMUNAS):
        # Realiza las verificaciones necesarias para agregar una comuna
        # tambien retorna el texto indicando si fue exitoso o no

        # Si el mensaje es valido (contiene el nombre del bot
        # y la comuna existe en COMUNAS)
        if NOMBRE_BOT in message:
            message = message.replace(NOMBRE_BOT,"").strip().title()
            if message not in COMUNAS:
                text = "Porfavor escribe un nombre de comuna valido\."
                return text
                
        fase = Fase().faseDeComuna(message)  # fase de la comuna en message
        # Si el usuario esta registrado
        if self.user_in_base(user_id):
            with self.covid_data_base() as base:
                # Se comprueba que si la comuna esta registrara para el usuario user_id
                if (message,) in base.getUserComunas(user_id):
                    text = f"La comuna *{message}* ya se encuentra registrada\."
                else:
                    # La comuna no se encuentra registrada
                    base.suscribe2Comuna(user_id, message, fase)
                    text = f"Comuna *{message}* agregada exitosamente \!"
        else:
            # Si el usuario no esta registrado
            with self.covid_data_base() as base:
                base.addUser(user_id)  # Se agrega el usuario a la base
                base.suscribe2Comuna(user_id, message, fase)
                text = f"Comuna *{message}* agregada exitosamente \!"


        return text


    def user_in_base(self, user_id):
        with self.covid_data_base() as base:
            if (user_id,) in base.getUsers():
                return True      
            else:
                return False





