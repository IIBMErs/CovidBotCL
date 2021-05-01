
import logging
from telegram import InlineKeyboardMarkup, Update
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from menus import Menu
from respuestas import Respuesta
# Cargar parametros
from bot_token import TOKEN


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Start of the bot
def start(update: Update, context: CallbackContext) -> int:
    
    # Get user 
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the conversation.")

    # Genera elementos del menu principal
    keyboard_menu_principal = menu.principal
    reply_markup = InlineKeyboardMarkup(keyboard_menu_principal)
    
    # Actualizar Mensaje
    update.message.reply_text("Bienvenido a CoronaBot Chile. ¿Que deseas hacer?",reply_markup=reply_markup)
    return FIRST

def menu_registro(update: Update, context: CallbackContext):
    # Entrega las opciones del menu registrarse
    query = update.callback_query
    query.answer()


    # Menu de registro
    keyboard_menu_registro = menu.registro
    reply_markup = InlineKeyboardMarkup(keyboard_menu_registro)

    # Comprueba la respuesta
    user_id = update.effective_user.id
    response_text = respuesta.registro_response(user_id)

    # Actualizar respuesta
    query.edit_message_text(response_text, reply_markup=reply_markup, parse_mode='MarkdownV2')
    
    



def main():
    # Create updater
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    
    # Start conversation
    conv_handler  = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            FIRST: [
                CallbackQueryHandler(menu_registro, "menu_registro")
                
            ]

        },
        fallbacks=[CommandHandler('start',start)]
    )

    # updates
    dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))    


    # Start the bot
    updater.start_polling()
    updater.idle()
    pass

if __name__ == "__main__":
    import os
    os.system('clear')

    # Event rulers
    FIRST, SECOND, THIRD, FORTH = range(4)

    # Contains and generates all the menus
    menu = Menu() 
    respuesta = Respuesta()


    main()