from telegram import InlineKeyboardButton


class Menu:


    @property
    def principal(self):
        # Elementos en el menu princiapl y sus callbacks
        info_menu = {"Registrarme" : "registrarme",
                    "Notificaciones" : "notificaciones",
                    "Datos" : "datos",
                    "Salir" : "salir"
        } 

        return self.generate_menu(info_menu)

    def generate_menu(self, info_menu):
        # Returns a list with Inline Keyboard

        keyboard = []
        for name, callback in info_menu.items():
            keyboard.append([InlineKeyboardButton(name, callback_data=callback )])

        return keyboard




if __name__ == "__main__":
    import os
    os.system('clear')
    
    menu = Menu()

