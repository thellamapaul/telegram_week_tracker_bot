import os
import sys
import telebot
import math
from datetime import datetime

#take input of bot api like 'python bot.pi num:str'
BOT_TOKEN = sys.argv[1]

#create bot
bot = telebot.TeleBot(BOT_TOKEN)

#progress bar with 10 blocks with shaded empty function
def progress10shade(percent):
    bar_len = 10
    filled_len = math.floor(bar_len * percent)
    bar = '█' * filled_len + '░' * (bar_len - filled_len)
    return bar

#progress bar with 15 blocks, partial and fully shade empty function
def progress15semishade(percent):
    bar_len = 15
    filled_len = math.floor(bar_len * percent)
    remainder = bar_len * percent - filled_len
    if remainder >= 0.5:
        bar = '█' * filled_len + '▒' + '░' * (bar_len - filled_len -1)
    else: 
        bar = '█' * filled_len + '░' * (bar_len - filled_len)
    return bar

#stolen progress bar function, each character represents 8 blocks, each block represents 100/96 percent
#doesn't look good in telegram
def progress12(percent):
    block_len = 96
    bar_len = 12
    eighths = [' ', '▏', '▎ ', '▍', '▌', '▋', '▊', '▉', '█']
    full_blocks = math.floor(bar_len * percent)
    remainder = math.floor(block_len * percent) % 8
    if full_blocks == bar_len:
        bar = '[' + eighths[8] * full_blocks + ']'
    else:
        bar = '[' + eighths[8] * full_blocks + eighths[remainder] + ' ' * (bar_len - full_blocks - 1) + ']'
    return bar

#is weekend function
def isweekend(now):
    if now.weekday() < 4 :
        return 0
    elif now.weekday() == 4 and now.hour < 17 :
        return 0
    elif now.weekday() == 4 and now.hour > 16 :
        return 1
    else:
        return 1
    
#days remaining function
def days_remaining(now):
    weekday = now.weekday()
    if weekday > 4 :
        days_remaining = 0
    else:
        days_remaining = 4 - now.weekday()
    return days_remaining

#hours remaining function
def hours_remaining(now):
    if now.hour < 8 :
        dayhours_remaining = 9
    elif now.hour > 17 :
        dayhours_remaining = 0
    else:
        dayhours_remaining = 16 - now.hour
    return dayhours_remaining

#minutes remaining function
def minutes_remaining(now):
    if now.hour < 8 :
        minutes_remaining = 0
    elif now.hour > 17 :
        minutes_remaining = 0
    else:
        minutes_remaining = 60 - now.minute
    return minutes_remaining

#tracker function
def tracker():    
    now = datetime.now()
    # test time
    #now = datetime(2023,4,27,16,14)
    weekend = isweekend(now)
    dailyhours = 9
    hourlyminutes = 60
    weeklyhours = 45

    if weekend == 1 : 
        week_percent = 1
    else:
        days = days_remaining(now)
        hours = hours_remaining(now)
        minutes = minutes_remaining(now)
        week_percent = (1-(days*dailyhours+hours+minutes/hourlyminutes)/weeklyhours)
    bar=progress15semishade(week_percent)
    return "the week is "+str("{:.1f}".format(week_percent*100))+"% complete\n"+bar

#respond time
@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.now()
    current_time = now.strftime("%a %H:%M:%S")
    bot.reply_to(message, current_time)

#respond tracker
@bot.message_handler(commands=['tracker'])
def send_time(message):
    bot.reply_to(message, tracker())

#respond echo
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "not a thing")

bot.infinity_polling()