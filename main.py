import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
import time

# online
engine = pyttsx3.init()

last_command_time = time.time()


def listen_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Скажите вашу команду: ")
        audio = r.listen(source)

    try:
        our_speech = r.recognize_google(audio, language="ru")
        print("Вы сказали: " + our_speech)
        return our_speech
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
        return ""
    except sr.RequestError:
        print("Ошибка сервиса распознавания речи")
        return ""


def do_this_command(message):
    global last_command_time
    message = message.lower()
    if "привет" in message:
        say_message("Привет, друг!")
        last_command_time = time.time()
    elif "vk" in message or 'вк' in message:
        open_link('https://vk.com')
        last_command_time = time.time()
    elif "одноклассники" in message:
        open_link('https://ok.ru')
        last_command_time = time.time()
    elif 'дискорд' in message or 'discord' in message:
        open_link('https://discord.com/app')
        last_command_time = time.time()
    elif "пока" in message:
        say_message("Пока!")
        exit()
    else:
        say_message("Команда не распознана!")


def open_link(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            webbrowser.open(url, new=2)
        else:
            say_message("Не удалось открыть ссылку")
    except requests.exceptions.RequestException:
        say_message("Не удалось открыть ссылку")


def say_message(message):
    print("Голосовой ассистент: " + message)
    engine.say(message)
    engine.runAndWait()


if __name__ == '__main__':
    try:
        waiting_mode = False
        while True:
            current_time = time.time()
            if current_time - last_command_time > 5:
                if waiting_mode is False:
                    say_message("Режим ожидания активирован")
                    waiting_mode = True
                else:
                    command = listen_command()
                    if command != "":
                        if "Джарвис" in command:
                            last_command_time = time.time()
                            waiting_mode = False
                            say_message("Режим ожидания отключен")
                            say_message("Слушаю, сэр")
            else:
                command = listen_command()
                do_this_command(command)
    except KeyboardInterrupt:
        pass