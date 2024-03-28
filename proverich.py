import vosk
import json
import pyaudio
import pyttsx3
import time
import requests
import webbrowser
import os
import datetime
import pygame
import random
import pyautogui
from bs4 import BeautifulSoup
from selenium import webdriver

# offline
engine = pyttsx3.init()

stopped = False

current_time = datetime.datetime.now()
current_hour = current_time.hour

last_command_time = time.time()

modelbigru = r"vosk-model-ru-0.42"
modelsmallru = r"vosk-model-small-ru-0.22"
model = vosk.Model(modelsmallru)
rec = vosk.KaldiRecognizer(model, 16000)

ope = {
    0: r'music\open.wav',
    1: r'music\opencer.wav',
    2: r'music\loadcer.wav',
    3: r'music\load.wav'
}

chunk = 4000

pygame.init()

favorite = 'https://www.youtube.com/watch?v=JFUawBGHAtQ'
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=chunk)


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


def speek(play):
    global stopped
    pygame.mixer.music.load(play)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def open_speek():
    rand = random.randint(0,3)
    speek(ope[rand])


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


def do_this_command(message):
    global last_command_time
    message = message.lower()
    if ("привет" in message
            or "доброе утро" in message
            or "добрый день" in message
            or "добрый вечер" in message):
        if 6 <= current_hour < 12:
            speek(r'music\goodmorning.wav')
            print("Голосовой ассистент: Доброе утро")
        elif 12 <= current_hour < 18:
            speek(r'music\goodday.wav')
            print("Голосовой ассистент: Добрый день")
        else:
            speek(r'music\goodevening.wav')
            print("Голосовой ассистент: Добрый вечер")
        last_command_time = time.time()
    elif 'блокнот' in message and ('открой' or 'открывай') in message:
        os.system("C:/Windows/System32/notepad.exe")
        open_speek()
        last_command_time = time.time()
    elif (("vk" in message or ' вк ' in message or 'в контакте' in message)
          and ('открой' in message or 'открывай' in message)):
        open_link('https://vk.com')
        open_speek()
        last_command_time = time.time()
    elif "одноклассники" in message and ('открой' or 'открывай'):
        open_link('https://ok.ru')
        open_speek()
        last_command_time = time.time()
    elif (('дискорд' in message or 'discord' in message
           or 'игровой мессенджер' in message)
          and ('открой' or 'открывай')):
        open_link('https://discord.com/app')
        open_speek()
        last_command_time = time.time()
    elif ("ютуб" in message or "ютюб" in message) and ('открой' or 'открывай'):
        open_link('https://www.youtube.com')
        open_speek()
        last_command_time = time.time()
    elif (('король и шут' in message or 'короля и шута' in message)
          and ('лужники' in message or ('в' in message and 'лужниках' in message))
          and 'концерт' in message):
        open_link('https://www.youtube.com/watch?v=JFUawBGHAtQ')
        open_speek()
        last_command_time = time.time()
    elif 'протокол' in message and 'программист' in message:
        open_speek()
        last_command_time = time.time()
        os.system(f'start chrome https://beta.theb.ai/home {favorite}')
        time.sleep(5)
        pyautogui.hotkey('win', 'right')
    elif 'новост' in message and 'ковров' in message:
        open_speek()
        last_command_time = time.time()
        url = 'https://vk.com/podslushanokovrov1'
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        post_blocks = soup.find_all('div', {'class': 'wall_post_text'})
        for index, post in enumerate(post_blocks, start=1):
            text_inside_block = post.get_text()
            say_message(f'Пост {index}:\n{text_inside_block}\n')
            comma = listen_command()  # Слушаем команду
            message = comma.lower()
            if 'стоп' in message:
                say_message("Произошел выход из цикла по команде 'стоп'")
                break
        driver.quit()
        last_command_time = time.time()
    elif " пока " in message or "пока " in message or "пока" in message:
        speek(r'music\bye.wav')
        exit()
    elif 'валер' in message:
        last_command_time = time.time()
        speek(r'music/listencer.wav')
        print("Голосовой ассистент: Слушаю, сэр")
    else:
        say_message("Команда не распознана!")


if __name__ == '__main__':
    print('Говорите...')
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
                        if "валер" in command:
                            last_command_time = time.time()
                            waiting_mode = False
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
