from dotenv import load_dotenv
import os
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
import dialogflow_v2 as dialogflow
import logging

logger = logging.getLogger(__file__)


class TgLogHandler(logging.Handler):

    def __init__(self, tg_bot, user_chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.user_chat_id = user_chat_id

    def emit(self, record):
        msg_to_bot = self.format(record)
        self.tg_bot.send_message(chat_id=user_chat_id,
                                 text=msg_to_bot)


def detect_intent_texts(dialogflow_project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(dialogflow_project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)

    return response.query_result.fulfillment_text


def start(bot, update):
    message = update.message.text
    if message == '/start':
        text = 'Здравствуйте!'

        bot.send_message(chat_id=user_chat_id, text=text)


def reply(bot, update):
    message = update.message.text
    try:
        text = detect_intent_texts(dialogflow_project_id, session_id, message,
                                   language_code)
    except Exception as err:
        logger.error(err, exc_info=True)
    else:
        bot.send_message(chat_id=user_chat_id, text=text)


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    user_chat_id = os.getenv('TG_USER_CHAT_ID')
    google_application_credentials = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS')
    dialogflow_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = user_chat_id
    language_code = 'ru'
    bot = Bot(token=tg_bot_token)
    log_handler = TgLogHandler(bot, user_chat_id)
    logger.addHandler(log_handler)

    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher
    command_handler = MessageHandler(Filters.command, start)

    text_handler = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(command_handler)
    dispatcher.add_handler(text_handler)
    updater.start_polling()
