# Бот, обучаемый нейросетью

Бот может отвечать на сообщения в группе Вконтакте и в Телеграм, что значительно сократит время ожидания ответа.

Пример для Telegram:  
![Картинка][image1]  

Пример для ВКонтакте:  
![Картинка][image2]


### Как обучить бота
1. Создайте файл `questions.json` с вопросами и ответами. Файл должен иметь следующую структуру:
    ```
    {    
        "Тема1": {
            "questions": [
                "Вопрос1",
                "Вопрос2",
                ...
            ],
            "answer": "Ответ"
        },
   
        "Тема2": ...
        ...
    ...
    }
    ```
    Пример:
    ```
    { 
        "Устройство на работу": {
            "questions": [
                "Как устроиться к вам на работу?",
                "Как устроиться к вам?",
                "Как работать у вас?"         
            ],
            "answer": "Если вы хотите устроиться к нам, напишите на почту мини-эссе о себе и прикрепите ваше портфолио."
        },
        ...
    ```
    
1. Создайте [проект на DialogFlow] и получите идентификатор проекта 
2. Создайте ["агента"]
3. Получите [JSON-ключ], переименуйте его в `google-credentials.json` и положите в корень проекта   
4. Запустите в консоли обучающий файл 
   ```
   python train_bot.py
   ```


### Как запустить ботов на Heroku

1. Зарегистрируйте приложение на [Heroku]
2. В созданном приложении во вкладке `Deploy`
привяжите Ваш github-репозиторий в `Deployment method`
и нажмите `Deploy Branch` внизу страницы
3. Во вкладке `Settings` подключите два пакета (Add buildpack):
    * `heroku/python`
    * `https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack`

3. Во вкладке `Settings` заполните переменные:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
   
   GOOGLE_CREDENTIALS=содержимое файла google-credentials.json
   
   DIALOGFLOW_PROJECT_ID=имя вашего проекта в dialogflow
   
   VK_ADMIN_ID=id администратора-хозяина приложения
   
   VK_BOT_TOKEN=токен группы вконтакте

   TG_BOT_TOKEN=токен телеграм-бота
   
   TG_USER_CHAT_ID=ваш chat_id в телеграм
   ```
4. Во вкладке `Resources` запустите сервер  
   Можно запустить сразу двух ботов


### Как запустить на своей машине

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

1. Создайте в корневой папке файл ```.env``` и пропишите в нем переменные следующим образом:  
    ```
    GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
    GOOGLE_CREDENTIALS=содержимое файла google-credentials.json
    DIALOGFLOW_PROJECT_ID=имя вашего проекта в dialogflow
    VK_ADMIN_ID=id администратора-хозяина приложения
    VK_BOT_TOKEN=токен группы вконтакте
    TG_BOT_TOKEN=токен телеграм-бота
    TG_USER_CHAT_ID=ваш chat_id в телеграм
    ```

2. Запустите ботов: ```python pb_house_tg_bot_helper.py``` или ```python pb_house_vk_bot_helper.py```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков 
[dvmn.org](https://dvmn.org/modules/chat-bots/lesson/support-bot/).

[проект на DialogFlow]: https://cloud.google.com/dialogflow/docs/quick/setup/ 
["агента"]: https://cloud.google.com/dialogflow/docs/quick/build-agent
[JSON-ключ]: https://cloud.google.com/docs/authentication/getting-started


[Heroku]: https://id.heroku.com/login "Heroku"


[image1]: https://dvmn.org/filer/canonical/1569214094/323/
[image2]: https://dvmn.org/filer/canonical/1569214089/322/
