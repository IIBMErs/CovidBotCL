from covidsqlbase  import CovidDataBase
from parameters import PATH_LISTA_COMUNAS, NOMBRE_BOT, INFO_DATOS
import pandas as pd
from fases import Fase
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from send import Enviar


class Respuesta:

    def __init__(self):
        self.covid_data_base = CovidDataBase
        self.info_datos = INFO_DATOS

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


    def borrar_comuna_response(self, user_id, message, COMUNAS):
        # Comprobar que el nombre de la comuna este en message
        if message not in COMUNAS:
            text = "Porfavor escribe un nombre de comuna valido\."
            return text

        # Si el usuario se encuentra registrado
        if self.user_in_base(user_id):
            with self.covid_data_base() as base:
                # Se comprueba que si la comuna esta registrara para el usuario user_id
                if (message,) in base.getUserComunas(user_id):
                    base.unsuscribeComuna(user_id, message)
                    text = f"La comuna *{message}* se borro con exito\."
                else:
                    text = f"Usted no se encuentra suscrito a la comuna *{message}*\."

     
        else:
            text = "No cuenta con comunas registradas\."
        return text



    def user_in_base(self, user_id):
        # Verifica si el usuario esta en la base
        with self.covid_data_base() as base:
            if (user_id,) in base.getUsers():
                return True      
            else:
                return False



    def notificaciones_call(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        nombre_dato = query['data']



        user_id = update.effective_user.id

        with self.covid_data_base() as base:
            user_data_suscription = base.getUserDatos(user_id)
            # Si el usuario no esta suscrito
            if user_data_suscription == []:
                base.suscribe2Dato(user_id, nombre_dato)
                query.edit_message_text("Suscrito exitosamente!")
            else:
                user_data_suscription  =[dato[0] for dato in user_data_suscription]
                if nombre_dato in user_data_suscription:
                    base.unsuscribeDato(user_id, nombre_dato)
                    query.edit_message_text("Notificación detenida exitosamente!")
                else:
                    base.suscribe2Dato(user_id, nombre_dato)
                    query.edit_message_text("Suscrito exitosamente!")

    def datos_call(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        user_id = update.effective_user.id
        nombre_dato = query['data']
        enviar = Enviar()


        with self.covid_data_base() as base:
            user_comunas = base.getUserComunas(user_id)
            for comuna in user_comunas:
                enviar.imagen(nombre_dato, comuna[0], user_id)
            query.edit_message_text("Enviado!")



    def enviar_notificaciones(self, datos_updated):
        enviar = Enviar()
        
        with self.covid_data_base() as base:
            users = base.getUsers()

            # Iterar sobre usuarios
            for user_id in users:
                # Obtener las comunas del usuario
                comunas = base.getUserComunas(user_id[0])
                if comunas == []:
                    continue

                # Obtener los datos suscritos del usuario
                datos = base.getUserDatos(user_id[0])
                if datos == []:
                    continue
                
                primer_mensaje = False
                # Itera sobre los datos
                for dato in datos: 
                    # Comprueba que el dato fue actualizo 
                    if dato[0] in datos_updated:
                        if primer_mensaje == False:
                            # Se encia el primer mensaje con tl tipo de data
                            texto = f"Enviando actualización: {self.dict_info_datos[dato[0]]} "
                            enviar.texto(user_id[0], texto)
                            primer_mensaje = True
                        
                        for comuna in comunas:
                            enviar.imagen(dato[0], comuna[0], user_id[0])
                        primer_mensaje = False

    @property
    def dict_info_datos(self):
        # Diccionario de INFO_DATOS
        dic = {}
        for info in self.info_datos:
            dic[info[1]] = info[0]
        return dic







