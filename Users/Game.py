import re
import sqlite3
import time


def start_game(bot, message):
    Game(bot, message)


class Game:
    def __init__(self, bot, message):
        self.bot = bot
        self.chat_id = message.chat.id
        self.user = message.from_user.id
        mes = message.text
        self.gamename = re.sub('\/\w+\s*', "", mes).strip()
        connection = sqlite3.connect('Games.db')
        cursor = connection.cursor()
        try:
            cursor.execute("select * from '{}'".format(self.gamename))
            self.resp = self.bot.send_message(self.chat_id, "Введите логин вашей команды")
            self.bot.register_next_step_handler(self.resp, self.authorization)
        except:
            self.resp = self.bot.send_message(self.chat_id, "Неверное название квеста")

    def authorization(self, message):
        connection = sqlite3.connect('Games.db')
        cursor = connection.cursor()
        login = re.sub('\/\w+\s*', "", message.text).strip()
        teams = cursor.execute('select * from Teams').fetchall()
        teams = [i for i in teams if i[0] == login]
        for i in self.bot.get_chat_administrators(self.chat_id):
            if i.status == 'creator':
                self.adm = i
        if teams:
            teams = list(teams[0])
            if teams[1] is None:
                teams[1:4] = [""] * 3
            if teams[1] == "":
                teams[1] = str(self.adm.user.id)
            if self.adm.user.id != message.from_user.id:
                self.bot.send_message(self.chat_id, "Логин команды должен вводить создатель группы")
                self.bot.register_next_step_handler(self.resp, self.authorization)
            elif self.gamename in teams[2].split(",") or str(self.adm.user.id) != teams[1]:
                self.bot.send_message(self.chat_id, "Данный квест недоступен")
            else:
                self.team = teams  # Хранит игры и поинты команды
                cursor.execute(
                    "UPDATE Teams SET creator = '{}' where name = '{}'".format(self.adm.user.id, self.team[0]))
                quests = cursor.execute('select * from {}'.format(self.gamename)).fetchall()
                for i in range(len(quests)):
                    quests[i] = [str(i + 1) + "-й вопрос. " + quests[i][0], quests[i][1]]
                self.qs = quests
                g = str(self.team[2]) + ',' + self.gamename
                if g[0] == ',':
                    g = g[1:]
                cursor.execute(
                    "UPDATE Teams SET games = '{}' where name = '{}'".format(g, self.team[0]))
                connection.commit()
                cursor.close()
                connection.close()
                self.idq = 0
                self.points = 0
                time.clock()
                self.process()
        else:
            self.bot.send_message(self.chat_id, "Логин неверный")

    def process(self):
        if self.idq < len(self.qs):
            self.bot.send_message(self.chat_id, self.qs[self.idq])
            self.bot.register_next_step_handler(self.resp, self.catch)
        else:
            self.final()

    def catch(self, message):
        if message.text.startswith("/ответ"):
            txt = re.sub("\/ответ\s*", "", message.text).strip().lower()
            if txt == self.qs[self.idq][1]:
                self.bot.send_message(self.chat_id, "Верно!")
                self.idq += 1
                self.process()
            else:
                self.bot.send_message(self.chat_id, "Неверно")
                self.bot.register_next_step_handler(self.resp, self.catch)
            self.points += 10
        else:
            self.bot.register_next_step_handler(self.resp, self.catch)

    def final(self):
        connection = sqlite3.connect('Games.db')
        cursor = connection.cursor()
        x = time.clock()
        x = str(int(x) + self.points)
        p = str(self.team[3]) + ',' + x
        if p[0] == ',':
            p = p[1:]
        cursor.execute("UPDATE Teams SET points = '{}' where name = '{}'".format(p, self.team[0]))
        self.bot.send_message(self.chat_id, "Количество набранных баллов: " + x)
        self.bot.send_message(self.chat_id, "Конец игры")
        cursor.close()
        connection.commit()
        connection.close()
