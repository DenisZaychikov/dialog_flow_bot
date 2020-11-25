from dotenv import load_dotenv
import os
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
import dialogflow_v2 as dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)

    return response.query_result.fulfillment_text


def reply(bot, update):
    message = update.message.text
    if message == '/start':
        text = 'Здравствуйте!'
    else:
        text = detect_intent_texts(project_id, session_id, message,
                                   language_code)
    bot.send_message(chat_id=user_chat_id, text=text)


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    user_chat_id = os.getenv('TG_USER_CHAT_ID')
    google_application_credentials = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS')
    project_id = os.getenv('PROJECT_ID')
    session_id = user_chat_id
    language_code = 'ru'
    bot = Bot(token=tg_bot_token)

    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher
    handler = MessageHandler(Filters.all, reply)
    dispatcher.add_handler(handler)
    updater.start_polling()
