import telebot
from fuzzywuzzy import fuzz
import os
from pydub import AudioSegment
from time import sleep
import requests

def compare(a,b):
    for i in a:
        if fuzz.partial_ratio(i,b) > 80:
            return 1 
TOKEN = '1473701302:AAHdrETRWTGIyVvhJBXlIg3oqFvYmH3uxys'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Я -  8D Music Bot. \n Отправь музыку в формтае mp3, и подожди пару секунд \n Нахожусь в разработке и становлюсь лучше каждый день...')
@bot.message_handler(content_types=['text'])
def menu(message):
    if compare(['конвертировать','8D','8д','музыка','аудио','звук'], message.text.lower())==1:
        bot.send_message(message.chat.id, 'Отправь музыку в формтае mp3, чтобы конвертировать музыку в 8D версию')
    else:
        bot.send_message(message.chat.id, 'Скажи мне, я что похож на бота-собеседника или же умного ассистента? Отправь музыку в формтае mp3, чтобы конвертировать музыку в 8D версию')
@bot.message_handler(content_types=['audio'])
def choose(message):
    file_info = bot.get_file(message.audio.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
    with open('input.mp3','wb') as f:
        f.write(file.content)
    call = bot.send_message(message.chat.id, 'Введите название музыки которую вы хотите получить:')
    bot.register_next_step_handler(call, name)
def name(message):
    if str(type(message.text))=="<class 'str'>":
        global musicname
        musicname = message.text + ".mp3"
        call2 = bot.send_message(message.chat.id,"Чтобы запустить процесс визуализации пришлите любое сообщение...")
        bot.register_next_step_handler(call2, render)
    else:
        call = bot.send_message(message.chat.id, 'Введите только текст!  (название музыки которую вы хотите получить)')
        bot.register_next_step_handler(call, name)

def render(message):
    bot.send_message(message.chat.id, "Rendering...")
    print("rendering...")
    sound = AudioSegment.from_mp3("input.mp3")
    adjust_jump =8
    segment_length = 200
    _8d = sound[0]
    pan_limit=[]
    limit_left  = -100
    print("ready 1")
    bot.send_message(message.chat.id, 'Готовность 15%')
    for i in range(100):
        if int(limit_left) >= 100:
            break
        pan_limit.append(limit_left)
        limit_left+=adjust_jump
    pan_limit.append(100)
    print("ready 2")
    bot.send_message(message.chat.id, 'Готовность 30%')
    for i in range(0,len(pan_limit)):
        pan_limit[i] = pan_limit[i] /100
    sleep(2)
    c=0
    flag = True
    print("ready 3")
    bot.send_message(message.chat.id, 'Готовность 45%')
    for i in range(0,len(sound)-segment_length, segment_length):
        peice = sound[i:i+segment_length]
        if c==0 and not flag:
            flag =True
            c=c+2
        if c==len(pan_limit):
            c = c-2
            flag =False
        if flag:
            panned = peice.pan(pan_limit[c])
            c+=1
        else:
            panned = peice.pan(pan_limit[c])
            c-=1
        _8d =_8d+panned
    print("ready 100");
    bot.send_message(message.chat.id, 'Готовность 100%')
    print("SAVING")
    bot.send_message(message.chat.id, 'Сохранение...')
    out_f = open(musicname, 'wb')
    _8d.export(out_f, format='mp3')
    os.remove ('input.mp3')
    print("SENDING")
    bot.send_message(message.chat.id, 'Отправка...')
    result = open(musicname,"rb")
    bot.send_document(message.chat.id,result)
    result.close()
    os.remove(musicname)
    bot.send_message(message.chat.id, 'Спасибо что используете наш  сервис!  Это помогает нам развиваться.')
bot.polling(none_stop=True)
