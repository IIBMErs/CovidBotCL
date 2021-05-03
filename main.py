
import logging
from telegram import InlineKeyboardMarkup, Update
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from menus import Menu
from respuestas import Respuesta
from uuid import uuid4
# Cargar parametros
from bot_token import TOKEN
from parameters import NOMBRE_BOT
from parameters import INFO_DATOS
from parameters import PATH_COVID
from check_updates import CheckData


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


def start_over(update: Update, context: CallbackContext) -> None:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    query = update.callback_query
    query.answer()

    # Genera elementos del menu principal
    keyboard_menu_principal = menu.principal
    reply_markup = InlineKeyboardMarkup(keyboard_menu_principal)
    
    # Actualizar Mensaje
    query.edit_message_text(f"Bienvenido a {NOMBRE_BOT}. ¿Que deseas hacer?",reply_markup=reply_markup)
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

    

def ingresar_comuna(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Escriba @coronaChile_bot y posteriormente el nombre de la comuna para registrarla.")

def borrar_comuna(update: Update, context: CallbackContext):
    message_text = update.message.text.replace("/borrar","").title().strip()  # Nombre comuna
    user_id = update.message.from_user.id

    response_text = respuesta.borrar_comuna_response(user_id, message_text, COMUNAS)
    update.message.reply_text(response_text, parse_mode='MarkdownV2')

def eliminar_comuna(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Escriba /borrar seguido por nombre de la comuna para borrarla.")

def inlinequery_comunas(update: Update, context: CallbackContext):
    """Handle the inline query."""
    query = update.inline_query.query.lower()
    listaComunas = [c for c in COMUNAS if query in c.lower().strip()]

    results = [
        InlineQueryResultArticle(
            id=uuid4(), title=t, input_message_content=InputTextMessageContent(t), thumb_height=0, thumb_width=0
            ) for t in listaComunas       
    ]
    update.inline_query.answer(results)


def recivir_mensaje(update: Update, context: CallbackContext):
    # Recive inputs del usuario para agregar comunas
    
    message_text = update.message.text
    user_id = update.message.from_user.id
    
    response_text = respuesta.agregar_comuma_response(user_id, message_text, COMUNAS)
    update.message.reply_text(response_text, parse_mode='MarkdownV2')

def menu_notificaciones(update: Update, context: CallbackContext):
    # Entrega las opciones del menu de notificaciones
    query = update.callback_query
    query.answer()


    user_id = update.effective_user.id 
    keyboard_menu_notificaciones = menu.notificaciones(user_id)
    reply_markup = InlineKeyboardMarkup(keyboard_menu_notificaciones)

    query.edit_message_text("Selecciona aquellas que te quieres suscribir", reply_markup=reply_markup)

    return NOTIFICACIONES

def callbacks_notificaciones(update: Update, context: CallbackContext):
    datos_disponibles = [info[1] for info in INFO_DATOS]
    
    callbacks_list = []
    for dato in datos_disponibles:
        callbacks_list.append(CallbackQueryHandler(respuesta.notificaciones_call, pattern=dato))

    callbacks_list.append(CallbackQueryHandler(start_over, pattern='volver'))
    
    return callbacks_list


def menu_datos(update: Update, context: CallbackContext):
    # Entrega las opciones del menu de notificaciones
    query = update.callback_query
    query.answer()


    user_id = update.effective_user.id 
    keyboard_menu_datos = menu.datos(user_id)
    reply_markup = InlineKeyboardMarkup(keyboard_menu_datos)

    query.edit_message_text("Presiona el dato que quieras saber!", reply_markup=reply_markup)

    return DATOS

def callbacks_datos(update: Update, context: CallbackContext):
    datos_disponibles = [info[1] for info in INFO_DATOS]
    
    callbacks_list = []
    for dato in datos_disponibles:
        callbacks_list.append(CallbackQueryHandler(respuesta.datos_call, pattern=dato))

    callbacks_list.append(CallbackQueryHandler(start_over, pattern='volver'))
    
    return callbacks_list


def enviar_notificaciones(context: CallbackContext):
    
    (status_update, datos_updated) = check_data.check_nueva_data()

    if not status_update:   # si no hay nueva data return
        return

    respuesta.enviar_notificaciones(datos_updated)

    


    

def salir(update: Update, context: CallbackContext) -> None:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Gracias por usar {NOMBRE_BOT}. Te mantendremos informado!")

    return ConversationHandler.END


def main():
    # Create updater
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Notificaciones
    repeate = updater.job_queue
    repeate.run_repeating(enviar_notificaciones, first=1, interval=60, name="notificaciones")

    
    # Start conversation
    conv_handler  = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            PRINCIPAL: [
                CallbackQueryHandler(menu_registro, pattern="menu_registro"),
                CallbackQueryHandler(menu_notificaciones, pattern="notificaciones"),
                CallbackQueryHandler(menu_datos, pattern="datos"),
                CallbackQueryHandler(salir, pattern="salir"),
            ],
            REGISTRO: [
                CallbackQueryHandler(ingresar_comuna, pattern="ingresarComuna"),
                CallbackQueryHandler(eliminar_comuna, pattern="eliminarComuna"),
                CallbackQueryHandler(start_over, pattern="volver")
            ],
            NOTIFICACIONES: callbacks_notificaciones(Update, CallbackContext),
            DATOS: callbacks_datos(Update, CallbackContext)

        },
        fallbacks=[CommandHandler('start',start)]
    )

    # Command handler
    dispatcher.add_handler(CommandHandler('borrar',borrar_comuna))

    # updates
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(InlineQueryHandler(inlinequery_comunas))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, recivir_mensaje))    


    # Start the bot
    updater.start_polling()
    updater.idle()
    

if __name__ == "__main__":
    import os
    os.system('clear')

    # Event rulers
    PRINCIPAL, REGISTRO, NOTIFICACIONES, DATOS = range(4)

    # Contains and generates all the menus
    menu = Menu() 
    respuesta = Respuesta()
    COMUNAS = Respuesta().get_comunas
    check_data = CheckData(PATH_COVID, INFO_DATOS)

    main()