import requests
import dialogflow_v2 as dialogflow
import os
from dotenv import load_dotenv


def create_intent(project_id, training_phrases_parts, message_texts,
                  display_name):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)

        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = client.create_intent(parent, intent)


if __name__ == '__main__':
    load_dotenv()
    project_id = 'task3-dialog-flow'
    google_application_credentials = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS')

    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    resp = requests.get(url)
    resp.raise_for_status()
    texts = resp.json()

    for display_name in texts:
        training_phrases_parts = texts[display_name]['questions']
        message_texts = [texts[display_name]['answer']]
        create_intent(project_id, training_phrases_parts, message_texts,
                      display_name)
