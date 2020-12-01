import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__file__)


class VkLogHandler(logging.Handler):

    def __init__(self, vk_admin_id, vk_api):
        super().__init__()
        self.vk_admin_id = vk_admin_id
        self.vk_api = vk_api
        self.random_id = random.randint(1, 1000)

    def emit(self, record):
        msg_to_bot = self.format(record)
        self.vk_api.messages.send(
            user_id=self.vk_admin_id,
            random_id=self.random_id,
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


def send_message(event, vk_api, language_code, dialogflow_project_id):
    random_id = random.randint(1, 1000)
    text = event.text
    session_id = f'vk-{event.user_id}'
    try:
        message = detect_intent_texts(dialogflow_project_id, session_id, text,
                                      language_code)
        if message:
            vk_api.messages.send(
                user_id=event.user_id,
                random_id=random_id,
                message=message
            )
    except Exception as err:
        logger.exception(err)


if __name__ == "__main__":
    load_dotenv()
    google_application_credentials = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS')
    vk_bot_token = os.getenv('VK_BOT_TOKEN')
    dialogflow_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    vk_admin_id = os.getenv('VK_ADMIN_ID')
    language_code = 'ru'
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    log_handler = VkLogHandler(vk_admin_id, vk_api)
    logger.addHandler(log_handler)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_message(event, vk_api, language_code, dialogflow_project_id)
