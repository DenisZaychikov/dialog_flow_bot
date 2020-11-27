import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__file__)


class VkLogHandler(logging.Handler):

    def __init__(self, event, random_id, vk_api):
        super().__init__()
        self.user_id = event.user_id
        self.random_id = random_id
        self.vk_api = vk_api

    def emit(self, record):
        msg_to_bot = self.format(record)
        self.vk_api.messages.send(
            user_id=event.user_id,
            random_id=random_id,
            message=msg_to_bot
        )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def echo(event, vk_api, language_code, project_id, random_id):
    text = event.text
    try:
        message = detect_intent_texts(project_id, random_id, text,
                                      language_code)
    except Exception as err:
        logger.error(err, exc_info=True)
    else:
        if message:
            vk_api.messages.send(
                user_id=event.user_id,
                random_id=random_id,
                message=message
            )


if __name__ == "__main__":
    load_dotenv()
    google_application_credentials = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS')
    vk_bot_token = os.getenv('VK_BOT_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    language_code = 'ru'
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            random_id = random.randint(1, 1000)
            log_handler = VkLogHandler(event, random_id, vk_api)
            logger.addHandler(log_handler)
            echo(event, vk_api, language_code, project_id, random_id)
