#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import telebot
import config
import os
import time
import random
from Users.Users import SuperUser, User, Admin, get_users
from Users.shedule import start
from Users.Game import start_game
import _thread

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda message: message.chat.type == "group", commands=['quest'])
def game(message):
    start_game(bot, message)


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('music/'):
        f = open("music/" + file, 'rb')
        res = bot.send_voice(message.chat.id, f, None)
        print(res)
        time.sleep(3)


@bot.message_handler(commands=['admin'])
def be_admin(message):
    pw = message.text.split(" ", 1)[1]
    if pw == config.password:
        bot.send_message(message.chat.id,
                         "Здравствуйте, {} {}".format(message.from_user.first_name, message.from_user.last_name))
        if not get_users().admins_list:
            Admin(bot, message)


@bot.message_handler(commands=['start'])
def be_admin(message):
    uid = message.from_user.id
    bot.send_message(uid, "Здравствуйте, {} {}".format(message.from_user.first_name, message.from_user.last_name))
    if get_users().ismember(uid):
        bot.send_message(uid, "Для получения списка команд введите /помощь")
    else:
        bot.send_message(uid, "Так вы не зарегестрированы как пользователь, функциолнал бота вам недоступен")


def ca(message):
    b = not (message.chat.id in get_users().active_users)
    d = message.chat.type == "private"
    c = get_users().ismember(message.chat.id)
    return b * c * d


@bot.message_handler(func=lambda message: ca(message), content_types=['text'])
def check_answer(message):
    idu = message.chat.id
    if message.text == '/помощь':
        SuperUser(bot, message).help()
    elif message.text.startswith("/"):
        if idu in get_users().admins_list:
            Admin(bot, message)
        else:
            User(bot, message)


if __name__ == '__main__':
    random.seed()
    _thread.start_new_thread(start, (bot,))
    bot.polling(none_stop=True)