import telebot
import requests
import json
from random import randint


API_TOKEN = "5869258352:AAFWyt-J3nk2T3rHVjOaLqwwo6NXMV6M3NM"
bot = telebot.TeleBot(token=API_TOKEN)
API_WEATHER = '96db9f2d7a8c694a18e79b71adcfbe49'



@bot.message_handler(commands=['start'])
def welcome_activity(message):
    bot.send_message(message.chat.id, f'<b>Привет</b>, {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      'Воспользуйся командой <u>/help</u>, чтобы получить информацию о возиожном взаимодействии',
                     parse_mode='html')


@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id, 'Help information:\n /game - игра "Угадай число"\n'
                                      '/weather - расскажет о погоде')


@bot.message_handler(commands=['game'])
def guess_game(message):
    bot.send_message(message.chat.id, "Угадайте число от 1 до 10, у вас 5 попыток!")
    ans = randint(1, 10)
    try_num = 1
    bot.register_next_step_handler(message, guess_game_1, ans, try_num)


@bot.message_handler(commands=['weather'])
def weather_info_ask(message):
    bot.send_message(message.chat.id, "Назовите город, в котором хотели бы узнать погоду")
    bot.register_next_step_handler(message, weather_info_ans)


def guess_game_1(message, ans: int, try_num: int):
    if message.text.isdigit():
        n = int(message.text)
        if(ans == n):
            bot.send_message(message.chat.id, "Поздравляю! Вы угадали")
        else:
            if try_num > 4:
                bot.send_message(message.chat.id, "Попытки кончились :(")
                return
            if ans < n:
                bot.send_message(message.chat.id, f'Загаданное число меньше вашего')
            else:
                bot.send_message(message.chat.id, f'Загаданное число больше вашего')
            if try_num < 4:
                bot.send_message(message.chat.id, f'Осталось {5 - try_num} попытки')
            else:
                bot.send_message(message.chat.id, f'Осталось {5 - try_num} попытка')
            try_num += 1
            bot.register_next_step_handler(message, guess_game_1, ans, try_num)
    else:
        bot.send_message(message.chat.id, 'Вы ввели не число. Попробуйте еще раз.')
        bot.register_next_step_handler(message, guess_game, ans, try_num)





def weather_info_ans(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}'
                       f'&appid={API_WEATHER}&units=metric&lang=ru')
    data = json.loads(res.text)
    bot.send_message(message.chat.id, f'На данный момент погодa в городе {city.title()} {data["weather"][0]["description"]},'
                              f' температура: {data["main"]["temp"]}')


bot.polling(none_stop=True)
