САНЯ ДЛЯ ТЕБЯ ЕСЛИ ЧТО-ТО УМРЕТ https://developers.google.com/workspace/calendar/api/quickstart/python?hl=ru СОЗДАЕШЬ ВСЕ ПО ГАЙДУ ТОЛЬКО БЕЗ QUICKSTART.PY У ТЕБЯ HOSTAPI.PY,
ЧТО КАСАЕТСЯ СЕРВЕРА ТАМ ВЕЗДЕ УКАЗАН МОЙ СЕРВЕР https://infamously-busy-sandpiper.cloudpub.ru/oauth2callback ТЕБЕ НУЖЕН БУДЕТ ПУБЛИЧНЫЙ АДРЕСС ТВОЕГО КОТОРЫЙ ТЫ УКАЗЫВАЕШЬ ВМЕСТО И ЧТО ВАЖНО!!!!!
В ХОСТАПИ ЕСТЬ ТАКОЙ КОД flow = Flow.from_client_secrets_file(
    client_secrets_file = "credentials.json",
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"],
    redirect_uri = "https://infamously-busy-sandpiper.cloudpub.ru/oauth2callback"
)
REDIRECT_URI ЭТО ТВОЙ_ПУБЛИЧНЫЙ_АДРЕСС/oauch2callback!!!
И ЕЩЕ ПО ХОДУ МОИХ ДЕЙСТВИЙ Я ПОНЯЛ ЧТО ДЛЯ ГУГЛА ТЕБЕ НУЖЕН СВОЙ ГУГЛ АПИ ССЫЛКА ВЫШЕ УЖЕ ЕСТЬ! ТАМ КОГДА БУДЕШЬ СОЗДАВАТЬ ПОЛЬЗОВАТЕЛЯ ТЕБЕ НУЖЕН WEB USER!!! В REDIRECTED URIS ТЫ УКАЗЫВАЕШЬ СВОЮ ССЫЛКУ КАК И В КОДЕ!!!
ТАКЖЕ КОГДА СОЗДАЕШЬ ЮЗЕРА ТЕБЕ НАДО ЗАЧЕНИТЬ МОЙ ФАЙЛ CREDENTIALS НА СВОЙ ПРОСТО ПЕРЕИМЕНОВАВ USER_SERCET КОТОРЫЙ У ТЕБЯ СКАЧАЕТСЯ В ГАЙДЕ БОЛЕЕ ОПИСАНО Я ЕБАЛ В 5 УТРА СИЖУ

ПО ЗАПУСКУ НЕ СЛОЖНО СНАЧАЛА HOSTAPI.PY ДЛЯ САЙТА А ПОТОМ MAIN.PY БИБЛИОТЕКИ Я ВСЕ НЕ УКАЖУ КИНЬ В ЧАТ ГПТ ЛУЧШЕ И ПОПРОСИ СПИСОК БИБЛИОТЕК!

ТАКЖЕ МОЙ ГАЙД МБ ХУНЯ И ТЫ НЕ ПОЙМЕШЬ ЕСЛИ ТАК КИДАЙ ВСЕЕ В GPT И ПОПРОСИ ПОМОЧЬ С ЗАПУСОМ 
