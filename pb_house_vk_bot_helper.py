import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os


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


def echo(event, vk_api, language_code, project_id):
    text = event.text
    random_id = random.randint(1, 1000)
    vk_api.messages.send(
        user_id=event.user_id,
        random_id=random_id,
        message=detect_intent_texts(project_id, random_id, text, language_code)
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
            echo(event, vk_api, language_code, project_id)
