
import logging
from telegram import InlineKeyboardMarkup, Update
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from menus import Menu
from respuestas import Respuesta
from uuid import uuid4
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
    return PRINCIPAL

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
    return REGISTRO
    

def ingresarComuna(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Escriba @coronaChile_bot y posteriormente el nombre de la comuna para registrarla")

def inlinequery_comunas(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query.lower()
    listaComunas = [c for c in COMUNAS if query in c.lower().strip()]

    results = [
        InlineQueryResultArticle(
            id=uuid4(), title=t, input_message_content=InputTextMessageContent(t), thumb_height=0, thumb_width=0
            ) for t in listaComunas       
    ]
    update.inline_query.answer(results)


def main():
    # Create updater
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    
    # Start conversation
    conv_handler  = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            PRINCIPAL: [
                CallbackQueryHandler(menu_registro, "menu_registro")
                
            ],
            REGISTRO: [
                CallbackQueryHandler(ingresarComuna, "ingresarComuna")
            ]


        },
        fallbacks=[CommandHandler('start',start)]
    )

    # updates
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(InlineQueryHandler(inlinequery_comunas))


    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))    


    # Start the bot
    updater.start_polling()
    updater.idle()
    pass

if __name__ == "__main__":
    import os
    os.system('clear')

    # Event rulers
    PRINCIPAL, REGISTRO, THIRD, FORTH = range(4)

    # Contains and generates all the menus
    menu = Menu() 
    respuesta = Respuesta()
    COMUNAS = respuesta.get_comunas


    main()