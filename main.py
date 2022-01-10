import telebot
import psycopg2
from datetime import datetime

conn = psycopg2.connect(database="schedule_db",
                        user="postgres",
                        password="",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

token = '2121318074:AAHrqJRAFMKlQbyhWb9Px5diZkV6NTDeSiA'
bot = telebot.TeleBot(token)
ping_counter = 0

days_list = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
week_number = datetime.today().isocalendar()[1] % 2

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю")
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")
    bot.send_message(message.chat.id, "Расписание на какой день вы хотите увидеть?", reply_markup=keyboard)

@bot.message_handler(commands=['week'])
def weekNumber(message):
    if week_number == 1:
        bot.send_message(message.chat.id, "Сейчас идет нечетная неделя")
    else:
        bot.send_message(message.chat.id, "Сейчас идет четная неделя")

@bot.message_handler(commands=['mtuci'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Сайт МТУСИ: https://mtuci.ru/")

@bot.message_handler(commands=['help'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Описание доступных команд:\n"
                                      "/help - помощь по доступным командам\n"
                                      "/week - четная/нечетная неделя\n"
                                      "/mtuci - ссылка на официальный сайт МТУСИ\n"
                                      "Нажмите на кнопку нужного дня или недели для вывода расписания")

@bot.message_handler(commands=['ping'])
def weekNumber(message):
    global ping_counter
    if ping_counter < 2:
        bot.send_message(message.chat.id, "Pong!")
        ping_counter += 1
    elif ping_counter == 2:
        bot.send_message(message.chat.id, "Triple Pong!")
        ping_counter += 1
    elif ping_counter == 3:
        bot.send_message(message.chat.id, "Ultra Pong!!!")
        ping_counter += 1
    elif ping_counter == 4:
        bot.send_message(message.chat.id, "RAMPAGE PONG!!!")
        ping_counter = 0

@bot.message_handler(commands=['credits'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Bot by Edward Vishnevsky <3\n"
                                      "https://vk.com/edward.vishnevskii")

@bot.message_handler(content_types='text')
def reply(message):
    if message.text.lower() in days_list:
        if week_number == 1:
            cursor.execute(f"SELECT * FROM timetable where day = '{message.text.lower()} 1' or day = '{message.text.lower()} 0' order by start_time")
        else:
            cursor.execute(f"SELECT * FROM timetable where day = '{message.text.lower()} 2' or day = '{message.text.lower()} 0' order by start_time")
        records = list(cursor.fetchall())
        text = f"{message.text}:\n"
        text += '____________________________________________________________\n'
        for i in records:
            text += f"Предмет: {i[2]}; Кабинет: {i[3]}; Время: {i[4]}\n"
        text += "____________________________________________________________"
        bot.send_message(message.chat.id, text)
    elif 'текущую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            for j in records:
                text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]} \n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    elif 'следующую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number + 1 == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            for j in records:
                text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]} \n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")

bot.infinity_polling()
