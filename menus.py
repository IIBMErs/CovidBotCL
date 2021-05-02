from telegram import InlineKeyboardButton
from covidsqlbase import CovidDataBase
from parameters import INFO_DATOS

class Menu:

    @property
    def principal(self):
        # Elementos en el menu princiapl y sus callbacks
        info_menu = {"Registrarme" : "menu_registro",
                    "Notificaciones" : "notificaciones",
                    "Datos" : "datos",
                    "Salir" : "salir"
        } 

        return self.generate_menu(info_menu)

    @property
    def registro(self):
        # Elementos en el menu de registro y sus callbacks
        info_menu = {
            "Agregar Comuna": "ingresarComuna",
            "Eliminar Comuna": "eliminarComuna",
            "Volver": "volver"
        }
        return self.generate_menu(info_menu)

    def generate_menu(self, info_menu):
        # Returns a list with Inline Keyboard

        keyboard = []
        for name, callback in info_menu.items():
            keyboard.append([InlineKeyboardButton(name, callback_data=callback )])

        return keyboard


    def create_keyboard_datos(self, user_id=-1, incluir_enroller=False):
        with CovidDataBase() as base:
            user_data_suscription = base.getUserDatos(user_id) 
            user_data_suscription  =[dato[0] for dato in user_data_suscription]
            
            info_menu = {}
            for info in INFO_DATOS:
                if info[1] in user_data_suscription and incluir_enroller:
                    info_menu[info[0] + "  \U00002705"] = info[1]
                else:
                    info_menu[info[0]] = info[1]

        return info_menu

    def datos(self, user_id):
        info_menu = self.create_keyboard_datos(user_id, incluir_enrolled=False)
        return self.generate_menu(info_menu)

    def notificaciones(self, user_id):
        info_menu = self.create_keyboard_datos(user_id, incluir_enroller=True)
        return self.generate_menu(info_menu)


if __name__ == "__main__":
    import os
    os.system('clear')
    
    menu = Menu()

    menu.create_keyboard_datos()

