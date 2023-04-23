import os
import sys
import telebot
from datetime import datetime

#take input of bot api like 'python bot.pi num:str'
BOT_TOKEN = sys.argv[1]

#create bot
bot = telebot.TeleBot(BOT_TOKEN)

#respond time
@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.now()
    current_time = now.strftime("%a %H:%M:%S")
    bot.reply_to(message, current_time)

#respond tracker
@bot.message_handler(commands=['tracker'])
def send_time(message):
    now = datetime.now()
    #calc days remaining
    weekday = now.weekday()
    if weekday > 4 :
        days_remaining = 0
    else:
        days_remaining = 4 - now.weekday()
    #calc weekend
    if now.weekday() < 4 :
        weekend = 0
    elif now.weekday() == 4 and now.hour < 17 :
        weekend = 0
    elif now.weekday() == 4 and now.hour > 16 :
        weekend = 1
    else:
        weekend = 1
    #calc hours remaining in current day
    if now.hour < 8 :
        dayhours_remaining = 8
    elif now.hour > 17 :
        dayhours_remaining = 0
    else:
        dayhours_remaining = 16 - now.hour
    minutes_remaining = 60 - now.minute
    #calc hours remaining in week
    if weekend == 1 : 
        week_percent = 100
    else:
        week_percent = (1-(days_remaining*9+dayhours_remaining+minutes_remaining/60)/45)*100
    if weekend == 1 :
        bot.reply_to(message, "the week is 100% complete")
    else:
        response = "the week is "+str("{:.1f}".format(week_percent))+"% complete"
        bot.reply_to(message, response)

#respond echo
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "not a thing")

bot.infinity_polling()