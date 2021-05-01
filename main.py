
import logging
from telegram import InlineKeyboardMarkup, Update
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from menus import Menu

# Cargar parametros
from bot_token import TOKEN


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Event values
FIRST, SECOND, THIRD, FORTH = range(4)



# Start of the bot
def start(update: Update, context: CallbackContext) -> int:
    
    # Get user 
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the conversation.")

    # Genera elementos del menu principal
    menu_principal = Menu().principal
    respuesta = InlineKeyboardMarkup(menu_principal)
    
    # Actualizar Mensaje
    update.message.reply_text("Bienvenido a CoronaBot Chile. ¿Que deseas hacer?",reply_markup=respuesta)



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
    main()