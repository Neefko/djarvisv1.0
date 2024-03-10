import vosk
import json
import pyaudio
import pyttsx3
import time
import requests
import webbrowser

# offline
engine = pyttsx3.init()

last_command_time = time.time()

modelbigru = r"C:\Users\79004\vosk-model-ru-0.42"
modelsmallru = r"C:\Users\79004\vosk-model-small-ru-0.22"
model = vosk.Model(modelbigru)
rec = vosk.KaldiRecognizer(model, 16000)

chunk = 4000

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=chunk)


def say_message(message):
    print("Голосовой ассистент: " + message)
    engine.say(message)
    engine.runAndWait()


def do_this_command(message):
    global last_command_time
    message = message.lower()
    if "привет" in message:
        say_message("Привет, друг!")
        last_command_time = time.time()
    elif ("vk" in message or 'вк' in message) and ('открой' or 'открывай'):
        open_link('https://vk.com')
        last_command_time = time.time()
    elif "одноклассники" in message and ('открой' or 'открывай'):
        open_link('https://ok.ru')
        last_command_time = time.time()
    elif ('дискорд' in message or 'discord' in message) and ('открой' or 'открывай'):
        open_link('https://discord.com/app')
        last_command_time = time.time()
    elif "ютуб" in message and ('открой' or 'открывай'):
        open_link('https://www.youtube.com')
        last_command_time = time.time()
    elif ('король и шут' in message or 'короля и шута' in message) and ('лужники' in message or ('в' in message and 'лужниках' in message)) and 'концерт' in message:
        open_link('https://www.youtube.com/watch?v=JFUawBGHAtQ')
        last_command_time = time.time()
    elif "пока" in message:
        say_message("Пока!")
        exit()
    elif 'иван' in message:
        last_command_time = time.time()
        pass
    else:
        say_message("Команда не распознана!")


def listen_command(timeout=20):
    start_time = time.time()
    while time.time() - start_time < timeout:
        data = stream.read(chunk)
        if rec.AcceptWaveform(data):
            result = rec.Result()
            json_result = json.loads(result)
            text = json_result.get('text', "")
            if text == '':
                return 'error204'
            else:
                print("Вы сказали: " + text)
                return text


def open_link(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            webbrowser.open(url, new=2)
        else:
            say_message("Не удалось открыть ссылку")
    except requests.exceptions.RequestException:
        say_message("Не удалось открыть ссылку")


if __name__ == '__main__':
    say_message('Говорите...')
    try:
        waiting_mode = False
        while True:
            current_time = time.time()
            if current_time - last_command_time > 15:
                if waiting_mode is False:
                    say_message("Режим ожидания активирован")
                    waiting_mode = True
                else:
                    command = listen_command()
                    if command != "":
                        if "иван" in command:
                            last_command_time = time.time()
                            waiting_mode = False
                            say_message("Слушаю, сэр")
                            do_this_command(command)
            else:
                command = listen_command()
                if 'error204' in command:
                    pass
                else:
                    do_this_command(command)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
