import time
import sqlite3


def start(bot):
    Schedule(bot)


def s(i):
    h, m = i[0].split(":")
    m = int(m) + int(h) * 60
    return m


class Schedule:
    def __init__(self, bot):
        self.bot = bot
        while 1:
            self.sch = self.sch_list()
            self.sendm()
            time.sleep(600)

    def sch_list(self):
        connection = sqlite3.connect('Users/Users.db')
        cursor = connection.cursor()
        sc = cursor.execute('select * from schedule').fetchall()
        li = []
        for i in sc:
            i = i[0]
            sch = cursor.execute('select * from "sch_{}"'.format(i)).fetchall()
            sch = [list(j) + [i.replace("_", " ")] for j in sch]
            li += sch
        li.sort(key=s)
        for i in range(len(li)):
            h, m = li[i][0].split(":")
            li[i][0] = int(m) + int(h) * 60
        return li

    def current_time(self):
        tim = time.ctime(time.time()).split(" ")[3].split(":")[:-1]
        a, b = map(int, tim)
        tim = a * 60 + b
        return tim

    def lessten(self):
        li = [i[1:] + [i[0] - self.current_time()] for i in self.sch_list() if 0 < i[0] - self.current_time() <= 10]
        li = [[i[0] + "\n" + 'Место - ' + i[1], i[-2], i[-1]] for i in li]
        return li

    def sendm(self):
        connection = sqlite3.connect('Users/Users.db')
        cursor = connection.cursor()
        users = cursor.execute('select * from Users').fetchall()
        users = [[i[0], i[-2]] for i in users]
        for i in self.lessten():
            for j in users:
                if i[1] in j:
                    self.bot.send_message(j[0], "Через {} минут: ".format(i[2]) + i[0])
