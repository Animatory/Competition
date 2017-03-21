# -*- coding: utf-8 -*-
import time
import sqlite3
import re

at = ('/добавить_участника <Фамилия> <Имя> <Отчество>, <Группа>, <Место жительства> - добавляет пользователя в '
      'базу бота и предоставляет ему доступ пользовательскому функционалу бота и даёт возможность администраторам '
      'взаимодействовать с ним. После ввода этой команды нужно переслать боту любое сообщение этого пользователя. Если '
      'указали неверные данные, то команда /break прерывает выполнение команды \n'
      'Пример: "/добавить_участника Иванов Иван Иванович, 6 отряд биотехнологии, 20 комната" \n\n'

      '/добавить_администратора <Фамилия> <Имя> <Отчество>, <Телефон>, <Деятельность> - даёт пользователю права '
      'администратора. После ввода этой команды нужно переслать боту любое сообщение этого пользователя. Если '
      'указали неверные данные, то команда /break прерывает выполнение команды \n'
      'Пример: "/добавить_участника Иванов Иван Иванович, 8 800 888 8888, Вожатый 6 отряда" \n\n'

      '/установить_расписание <Группы> - добавляет расписаие для заданной группы. Можно указать одну или несколько '
      'групп через запятую. Если указать в качестве аргумента "*", то расписание будет добавлено для всех групп.\n'
      'Примеры: "/установить_расписание 6 отряд, 5 отряд" или "/установить_расписание *"\n'
      'После ввода этой команды посылается сообщение, содержащее в себе пояснения по вводу расписания. После этого, '
      'следуя форме, можете записывать расписание\n\n'

      '/создать_квест <Название квеста> - создаёт квест, в котором могут участвовать только команды.\n'
      'Пример: "/создать_квест Анатомия"'

      '/расписание <Группа> - выводит расписание указанной группы\n'
      'Пример: "/расписание 6 отряд"\n\n'

      '/сообщение <Группы>; <Сообщение> - посылает пользователям, принадлежащим к указанным группам сообщение. Если '
      'в качестве группы написать "*", то сообщение будет отправлено всем пользователям.\n '
      'Примеры: "/сообщение 6 отряд, 5 отряд; Сообщение" или "/сообщение *; Сообщение"\n\n'

      '/дать_ачивку (<ФИО пользователя>) <Ачивка> - даёт пользователю, указанному в скобках ачивку\n'
      'Пример: "/дать_ачивку (Иванов Иван Иванович) Неспящий"\n\n'

      '/ачивки <ФИО пользователя> - показывает список ачивок пользователя\n'
      'Пример: "/ачивки Иванов Иван Иванович"\n\n'

      '/имя <Имя> \n'
      '/фамилия <Фамилия>\n'
      '/отчество <Отчество>\n'
      '/номер <Номер телефона>\n'
      '/деятельность <Деятельность>\n'
      '/осебе <Краткая информация об администраторе>\n'
      'Группа команд выше позволяет администратору менять данные о себе, доступные пользователям. Желательно указывать '
      'реальные данные, чтобы ученики понимали, кто это.\n\n'

      '/где <Фамилия>, <Имя>, <Отчество>, <Группа> - показывает, где живет пользователь с указанными данными. Можно '
      'указать от 0 до 4 параметров. Порядок не имеет значение. Если таких пользователей несколько, то бот выводит '
      'их всех\n'
      'Примеры корректной команды: "/где Пётр", "/где 6 отряд", "/где Пётр, 6 отряд, Викторович \n\n'

      '/руководители - выдаёт список всех администраторов с информацией о них\n\n'
      '/участники - выдаёт список всех пользователей с информацией о них\n')

ut = ('/событие – выводит текущий и следующий пункт в расписании\n\n'

      '/ачивки <ФИО пользователя> - показывает список ачивок пользователя. При отсутствии ФИО выводит ачивки '
      'пользователя, вызвавшего команду. \n'
      'Пример корректной команды: "/ачивки Иванов Иван Иванович" или "/ачивки"\n\n'

      '/расписание <Группа> - выводит расписание указанной группы. При отсутствии группы выводит расписание '
      'пользователя, вызвавшего команду.\n'
      'Пример корректной команды: "/расписание 6 отряд"\n\n'

      '/где <Фамилия>, <Имя>, <Отчество>, <Группа> - показывает, где живет пользователь с указанными данными. Можно '
      'указать от 0 до 4 параметров. Порядок не имеет значение. Если таких пользователей несколько, то бот выводит '
      'их всех\n'
      'Примеры корректной команды: "/где Пётр", "/где 6 отряд", "/где Пётр, 6 отряд, Викторович \n\n'

      '/руководители - выдаёт список всех администраторов с информацией о них\n\n'
      '/участники - выдаёт список всех пользователей с информацией о них\n')


def current_time():
    tim = time.ctime(time.time()).split(" ")[3].split(":")[:-1]
    a, b = map(int, tim)
    tim = a * 60 + b
    return tim


class get_users:
    user_list = []
    admins_list = []
    active_users = {}

    def __init__(self):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        try:
            u = cursor.execute('select * from Users').fetchall()
        except sqlite3.OperationalError as y:
            u = []
        try:
            a = cursor.execute('select * from Admins').fetchall()
        except sqlite3.OperationalError as y:
            a = []
        self.user_list = [i[0] for i in u]
        self.admins_list = [i[0] for i in a]
        connection.close()

    def update(self):
        self.__init__()

    def ismember(self, uid):
        return uid in self.admins_list + self.user_list


class SuperUser:
    def __init__(self, bot, message):
        self.bot = bot
        self.user_id = message.from_user.id
        self.message = message

    def help(self):
        if self.user_id in get_users().admins_list:
            self.bot.send_message(self.user_id, at)
        else:
            self.bot.send_message(self.user_id, ut)

    def users(self, message):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        try:
            cursor.execute("""CREATE TABLE Users (
                            'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            'last_name'	TEXT NOT NULL,
                            'first_name'	TEXT NOT NULL,
                            'sub_name'	TEXT,
                            'group'	TEXT NOT NULL,
                            'where'	TEXT);""")
        except sqlite3.OperationalError:
            pass
        if message.startswith("/участники"):
            u = cursor.execute('select * from Users').fetchall()
            for i in range(len(u)):
                u[i] = list(u[i][1:])
                u[i][-1] = 'Место жительства: ' + u[i][-1]
                u[i][-2] = 'Группа: ' + u[i][-2]
                u[i][-3] = " ".join(u[i][:3])
        else:
            u = cursor.execute('select * from Admins').fetchall()
            for i in range(len(u)):
                u[i] = list(u[i][1:])
                u[i][-2] = 'Деятельность: ' + u[i][-2]
                u[i][-3] = 'Телефон: ' + u[i][-3]
                u[i][-4] = " ".join(u[i][:3])
        a = ["\n".join(i[2:]).strip() for i in u]
        return a

    def whereis(self, message):
        txt = re.sub('\/\w+\s*', "", message)
        us = SuperUser.users(self, "/участники")
        if txt == 0:
            self.bot.send_message(self.user_id, "\n\n".join(us))
            return None
        txt = re.split(',\s*', txt)
        ul = []
        for i in us:
            p = True
            for j in txt:
                p *= j in i
            if p:
                ul.append(i)
        if ul:
            ul = '\n\n'.join(ul)
            self.bot.send_message(self.user_id, ul)
        else:
            txt = "Участник не найден.\n" \
                  "Возможно, вы указали данные неверно, либо участника ещё не добавили в систему."
            self.bot.send_message(self.user_id, txt)

    def set_sth(self, message):
        message, keys, file = message
        key = message.split(" ", maxsplit=1)[0]
        message = re.sub('\/\w+\s*', "", message)
        if message == "":
            self.bot.send_message(self.user_id, "Не указан параметр")
            return None
        field = keys[key]
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        cursor.execute(file.format(field, message, self.user_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.bot.send_message(self.user_id, "Данные обновлены")

    def get_schedule(self, group):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        try:
            u = cursor.execute("select * from 'sch_{}'".format(group.replace(" ", "_"))).fetchall()
            u = "\n".join(['{} - {}, {}'.format(i[0], i[1], i[2]) for i in u])
            self.bot.send_message(self.user_id, u)
        except sqlite3.OperationalError:
            self.bot.send_message(self.user_id, "Расписание не установлено")
        connection.close()

    def achievement_list(self, name):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        if name:
            u = cursor.execute('select * from Achieve').fetchall()
            u = [" ".join(i[1:4]) + "\n" + i[-1] for i in u if i[1] in name and i[2] in name and i[3] in name]
            if u:
                self.bot.send_message(self.user_id, u[0])
            else:
                self.bot.send_message(self.user_id, "Пользователь не найден, либо у него не ачивок")
        else:
            u = cursor.execute('select * from Achieve where id = {}'.format(self.user_id)).fetchall()
            if u:
                u = u[0][1:]
                u = " ".join(u[:3]) + "\n" + u[-1]
                self.bot.send_message(self.user_id, u)
            else:
                self.bot.send_message(self.user_id, "У вас нет ачивок")

    def de(self):
        try:
            get_users().active_users.pop(self.user_id)
        except KeyError:
            pass


class User(SuperUser):
    def __init__(self, bot, message):
        super().__init__(bot, message)
        try:
            self.command = self.list_commands[message.text.split(" ")[0]]
            self.command(self, message=message.text)
        except KeyError:
            self.bot.send_message(self.user_id, "Неверная команда")
            self.bot.send_message(self.user_id, "Введите /help для получения списка с описанием команд")
            self.de()

    def achievement_list(self, message):
        message = re.sub('\/\w+\s*', "", message).strip()
        super().achievement_list(message)
        self.de()

    def get_schedule(self, message):
        try:
            group = message.split(" ")[1]
        except IndexError:
            connection = sqlite3.connect('Users.db')
            cursor = connection.cursor()
            group = cursor.execute('select * from Users where id = {}'.format(self.user_id)).fetchall()[0][4]
            cursor.close()
            connection.close()
        super().get_schedule(group)
        self.de()

    def current_event(self, message):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        group = cursor.execute('select * from Users where id = {}'.format(self.user_id)).fetchall()[0][4]
        try:
            u = cursor.execute("select * from 'sch_{}'".format(group.replace(" ", "_"))).fetchall()
            un = []
            ct = current_time()
            for i in range(len(u)):
                h, m = u[i][0].split(":")
                u[i] = list(u[i])
                u[i].append(int(m) + int(h) * 60)

            for i in range(len(u)):
                if i == 0 and u[i][-1] - ct > 0:
                    un.append("Текущее событие: нет")
                    un.append("Следующее событие: {} - {}, {}".format(u[i][0], u[i][1], u[i][2]))
                    break
                elif i + 1 == range(len(u)):
                    un.append("Текущее событие: {} - {}, {}".format(u[i][0], u[i][1], u[i][2]))
                    un.append("Следующее событие: нет")
                elif u[i][-1] - ct < 0 <= u[i + 1][-1] - ct:
                    un.append("Текущее событие: с {} - {}, {}".format(u[i][0], u[i][1], u[i][2]))
                    un.append("Следующее событие: {} - {}, {}".format(u[i + 1][0], u[i + 1][1], u[i + 1][2]))
            self.bot.send_message(self.user_id, "\n".join(un))
        except sqlite3.OperationalError:
            self.bot.send_message(self.user_id, "Расписание не установлено")
        connection.close()

    def get_contact(self, message):
        try:
            txt = message.split(" ")[1:]
        except IndexError:
            txt = " "
        us = SuperUser.users(self, "/руководители")
        ul = []
        for i in us:
            p = True
            for j in txt:
                p *= j in i
            if p:
                ul.append("\n".join(i.splitlines()[:2]))
        if ul:
            ul = '\n\n'.join(ul)
            self.bot.send_message(self.user_id, ul)
        else:
            txt = "Такого руководителя у нас нет)"
            self.bot.send_message(self.user_id, txt)
        self.de()

    def users(self, message):
        us = super().users(message)
        if us:
            self.bot.send_message(self.user_id, "\n\n".join(us))
        else:
            self.bot.send_message(self.user_id, "Участников нет")
        self.de()

    def whereis(self, message):
        super().whereis(message)
        self.de()

    list_commands = {
        '/событие': current_event,
        '/ачивки': achievement_list,
        '/расписание': get_schedule,
        '/где': whereis,
        '/руководители': users,
        '/участники': users
    }


class Admin(SuperUser):
    def __init__(self, bot, message):
        super().__init__(bot, message)
        get_users().active_users[self.user_id] = self.user_id

        if not (self.user_id in get_users().admins_list):
            txt = "Для завершения регистрации введите свои данные в следующем формате:\n" \
                  "<Фамилия> <Имя> <Отчество>, <Номер телефона>, <кратко о том, кто вы>\n" \
                  "Пример:\n Пупкин Василий Игоревич, 8-800-555-3535, Физик-ядерщик, вожатый 6 отряда"
            resp = self.bot.send_message(self.user_id, txt)
            self.bot.register_next_step_handler(resp, self.hello)
        else:
            try:
                self.command = self.list_commands[message.text.split(" ")[0]]
                self.command(self, message=message.text)
            except KeyError as a:
                self.bot.send_message(self.user_id, "Неверная команда")
                self.bot.send_message(self.user_id, "Введите /help для получения списка с описанием команд")
                self.de()

    def hello(self, message):

        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        try:
            txt = [i.strip() for i in message.text.split(",", maxsplit=2)]
            txt[:1] = txt[0].split(" ")
            txt = [self.user_id] + txt
            try:
                cursor.execute("""CREATE TABLE Admins (
                                            'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            'last_name'	TEXT NOT NULL,
                                            'first_name'	TEXT NOT NULL,
                                            'sub_name'	TEXT,
                                            'phone'	TEXT NOT NULL,
                                            'act'	TEXT,
                                            'about_me'	TEXT);""")
            except sqlite3.OperationalError:
                pass
            cursor.execute("insert into Admins values (?, ?, ?, ?, ?, ?, '')", txt)

            self.bot.send_message(self.user_id, "Вы зарегистрированы как администратор")
            self.bot.send_message(self.user_id, "Введите команду /help для получения справки о функциях бота")
        except:
            self.bot.send_message(self.user_id, "Неверный формат ввода")
        connection.commit()
        get_users().update()
        cursor.close()
        connection.close()
        self.de()

    def set_sth(self, message):  # изменяет данные администратора
        keys = {'/осебе': 'about_me', '/номер': 'phone', '/деятельность': 'act', '/имя': 'first_name',
                '/фамилия': 'last_name', '/отчество': 'sub_name'}
        file = "UPDATE Admins SET {} = '{}' where id = {};"
        me = [message, keys, file]
        super().set_sth(me)
        self.de()

    def give_achievement(self, message):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        pattern = re.compile('\(\w+\s\w+\s\w+\)')
        message = re.sub('\/\w+\s', "", message)

        name = pattern.findall(message)
        if not name:
            self.bot.send_message(self.user_id, "Неверный формат входных данных")
            self.de()
            return None
        else:
            name = name[0]
            name = name[1:-1].split(" ")
        ach = pattern.sub("", message).strip()
        if not ach:
            self.bot.send_message(self.user_id, "Не указана ачивка")
            self.de()
            return None
        us = cursor.execute('select * from Users').fetchall()
        us += cursor.execute('select * from Admins').fetchall()

        ul = []
        for i in us:
            p = True
            for j in name:
                p *= j in i
            if p:
                ul.append([i[0]] + name)
        if ul:
            ul = ul[0]
            ac = ach
            try:
                u = cursor.execute('select * from Achieve where id = {}'.format(ul[0])).fetchall()
                if u:
                    ach = re.split(',\s+', ach) + u[-1].split(", ")
                    ach.sort()
                    ach = ", ".join(ach)
                ul.append(ach)
            except sqlite3.OperationalError:
                cursor.execute("""CREATE TABLE 'Achieve' (
                'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                'lastn'	TEXT NOT NULL,
                'firstn'	TEXT NOT NULL,
                'subn'	TEXT NOT NULL,
                'ach_list'	TEXT);""")
            cursor.execute("insert into 'Achieve' values (?, ?, ?, ?, ?)", ul)
            connection.commit()
            self.bot.send_message(self.user_id, "Ачивка выдана")
            self.bot.send_message(ul[0], "Вы получили ачивку: '{}'".format(ac))
        else:
            txt = "Участник не найден.\n" \
                  "Возможно, вы указали данные неверно, либо участника ещё не добавили в систему."
            self.bot.send_message(self.user_id, txt)
        self.de()

    def users(self, message):
        us = super().users(message)
        if us:
            self.bot.send_message(self.user_id, "\n\n".join(us))
        else:
            self.bot.send_message(self.user_id, "Участников нет")
        self.de()


    def whereis(self, message):
        super().whereis(message)
        self.de()

    def give_message(self, message):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        try:
            message = re.sub('\/\w+\s*', "", message)
            if message == "":
                raise IndexError
        except IndexError:
            self.bot.send_message(self.user_id, "Не указаны группа и сообщение")
            self.de()
            return None
        message = [i.strip() for i in message.split(";", maxsplit=1)]
        if len(message) == 1:
            self.bot.send_message(self.user_id, "Неверный формат вводимых данных")
            self.de()
            return None
        elif message[1] == "":
            self.bot.send_message(self.user_id, "Нельзя отправить пустое сообщение")
            self.de()
            return None
        groups = message[0]
        message = message[1]
        u = cursor.execute('select * from Users').fetchall()
        ids = [[i[0], i[4]] for i in u]
        u = set([i[4] for i in u])
        if groups == "*":
            groups = u
        else:
            groups = [i.strip() for i in groups.split(",")]
            for i in groups:
                if not (i in u):
                    self.bot.send_message(self.user_id, "Неверно указанна группа(ы)".format(i))
                    self.de()
                    return None
        for i in ids:
            if i[1] in groups:
                self.bot.send_message(i[0], message)
        self.bot.send_message(self.user_id, "Сообщение отправлено")

    def set_schedule(self, message):
        txt = "Для корректного составения расписания придерживайтесь следующей формы:\n" \
              "1) Отрправляйте один пункт расписания в одном сообщении, либо разделяйте их переносом строки \n" \
              "2) Формат записы пункта: <час>:<минута> - <событие>, <место>\n" \
              "3) Команда /end завершает ввод и сохраняет расписание\n" \
              "4) Команда /break прерывает ввод, расписание не сохраняется\n"
        try:
            self.groups = message.split(" ", maxsplit=1)[1]
        except IndexError:
            self.bot.send_message(self.user_id, "Не указана группа!")
            self.de()
            return None
        self.resp = self.bot.send_message(self.user_id, txt)
        self.bot.register_next_step_handler(self.resp, self.schedule)
        self.sch = []

    def schedule(self, message):
        if message.text.startswith('/end'):
            connection = sqlite3.connect('Users.db')
            cursor = connection.cursor()
            try:
                cursor.execute("""CREATE TABLE 'schedule' ('name' TEXT NOT NULL UNIQUE);""")
            except sqlite3.OperationalError:
                pass

            if self.groups == "*":
                u = cursor.execute('select * from Users').fetchall()
                self.groups = [i[4] for i in u]
            else:
                self.groups = [i.strip() for i in self.groups.split(",")]

            for j in self.groups:
                j = j.replace(" ", "_")
                try:
                    cursor.execute("insert into 'schedule' values (?)", (j,))
                except sqlite3.IntegrityError:
                    pass
                try:
                    cursor.execute("delete from 'sch_{}' where 1 = 1".format(j))
                    [cursor.execute("insert into 'sch_{}' values (?, ?, ?)".format(j), i) for i in self.sch if
                     i != [""]]
                except sqlite3.OperationalError:
                    cursor.execute("""CREATE TABLE 'sch_{}' (
                                    'time'	TEXT NOT NULL UNIQUE,
                                    'action'	TEXT NOT NULL,
                                    'place'	TEXT NOT NULL);""".format(j))
                    [cursor.execute("insert into 'sch_{}' values (?, ?, ?)".format(j), i) for i in self.sch if
                     i != [""]]
            connection.commit()
            u = cursor.execute('select * from Users').fetchall()
            u = [i[0] for i in u if i[4] in self.groups]
            self.message.text = "/расписание"
            for i in u:
                self.message.from_user.id = i
                User(self.bot, self.message)
            cursor.close()
            connection.close()
            self.bot.send_message(self.user_id, "Расписание сохранено")
            self.de()
        elif message.text.startswith("/break"):
            self.de()
        else:
            try:
                txt = message.text.splitlines()
                txt = [list(map(str.strip, i.strip().split(" - "))) for i in txt if i]
                txt = [[i[0]] + list(map(str.strip, i[1].split(', '))) for i in txt]
                self.sch += txt
                self.bot.register_next_step_handler(self.resp, self.schedule)
            except:
                self.bot.send_message(self.user_id, "Неверный формат входных данных")
                self.de()

    def get_schedule(self, message):
        group = re.sub('\/\w+\s*', "", message)
        if group:
            super().get_schedule(group)
        else:
            self.bot.send_message(self.user_id, "Укажите группу(ы)")
        self.de()

    def achievement_list(self, message):
        message = re.sub('\/\w+\s*', "", message).strip()
        super().achievement_list(message)
        self.de()

    def add_user(self, message):
        try:
            key, message = message.split(" ", maxsplit=1)
            name, fir, sec = [i.strip() for i in message.split(",", maxsplit=2)]
            name = name.split(" ")
            self.message = name + [fir, sec]
            resp = self.bot.send_message(self.user_id,
                                         "Перешлите в этот диалог любое сообщение пользователя, которого хотите добавить")
            if key == '/добавить_участника':
                self.bot.register_next_step_handler(resp, self.au)
            else:
                self.bot.register_next_step_handler(resp, self.aa)
        except ValueError:
            self.bot.send_message(self.user_id, "Неверный формат входных данных")
            self.de()

    def au(self, message):
        if message.text.startswith("/break"):
            self.bot.send_message(self.user_id, "Запись прервана")
            self.de()
            return None
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        new_id = message.forward_from.id
        txt = [new_id] + self.message
        try:
            cursor.execute("""CREATE TABLE Users (
                            'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            'last_name'	TEXT NOT NULL,
                            'first_name'	TEXT NOT NULL,
                            'sub_name'	TEXT,
                            'group'	TEXT NOT NULL,
                            'where'	TEXT);""")
        except sqlite3.OperationalError:
            pass
        try:
            with connection:
                connection.execute("insert into Users values (?, ?, ?, ?, ?, ?)", txt)
                self.bot.send_message(self.user_id, "Пользователь добавлен")
                self.bot.send_message(new_id, "Вы добавлены как пользователь")
                connection.commit()
                get_users().update()
        except sqlite3.IntegrityError:
            self.bot.send_message(self.user_id, "Этот пользователь уже добавлен")
        self.de()

    def aa(self, message):
        if message.text.startswith("/break"):
            self.bot.send_message(self.user_id, "Запись прервана")
            self.de()
            return None
        connection = sqlite3.connect('Users.db')
        new_id = message.forward_from.id
        txt = [new_id] + self.message
        try:
            with connection:
                connection.execute("insert into Admins values (?, ?, ?, ?, ?, ?, '')", txt)
                self.bot.send_message(self.user_id, "Администратор добавлен")
                self.bot.send_message(new_id, "Вы добавлены как администратор")
                connection.commit()
                get_users().update()
        except sqlite3.IntegrityError:
            self.bot.send_message(self.user_id, "Этот пользователь уже добавлен")
        self.de()

    def set_game(self, message):
        message = re.sub('\/\w+\s*', "", message).strip()
        self.gamename = message
        resp = self.bot.send_message(self.user_id, "Введите через ',' названия команд, участвующих в квесте")
        self.bot.register_next_step_handler(resp, self.set_teams)
        self.questions = []
        self.ind = -1

    def set_teams(self, message):
        connection = sqlite3.connect('Games.db')
        cursor = connection.cursor()
        teams = message.text
        try:
            cursor.execute("CREATE TABLE 'Teams' ("
                           "'name'	TEXT NOT NULL UNIQUE,"
                           "'creator''	TEXT,"
                           "'games'	TEXT,"
                           "'points'	TEXT,"
                           "PRIMARY KEY('name'));")
        except:
            pass
        teams = re.split("\,\s*", teams)
        print(teams)
        for i in teams:
            try:
                cursor.execute("insert into 'Teams' values (?, '', '', '')", [i])
            except Exception as u:
                print(u)
        self.resp = self.bot.send_message(self.user_id, "Если указали команду(ы) неверно, то введите '/break'")
        t = "При составлении квеста придерживайтесь следующим правилам:\n" \
            "1) Вопрос и ответ на него отправляйте боту в одном сообщении, разделив их знаком переноса строки.\n" \
            "2) При обнаружении ошибки в одном из отправленных вопросов, введите команду '/переписать <Номер вопроса>'," \
            "а в следующем сообщении исправленный вариант. Отсчёт вопросов начинается с 1 :)\n" \
            "3) Команда /end завершает ввод и сохраняет квест.\n" \
            "4) Команда /break прерывает ввод, квест не сохраняется.\n"
        self.bot.send_message(self.user_id, t)
        self.bot.register_next_step_handler(self.resp, self.set_question)
        connection.commit()
        cursor.close()
        connection.close()

    def set_question(self, message):
        if message.text.startswith("/break"):
            self.de()
            return None
        elif message.text.startswith("/переписать"):
            n = re.sub('\/переписать\s*', "", message.text).strip()
            try:
                n = int(n)
                if 0 < n <= len(self.questions):
                    self.ind = n - 1
                    self.bot.register_next_step_handler(self.resp, self.set_question)
                else:
                    self.bot.send_message(self.user_id, "Неверно указан номер")
                    self.bot.register_next_step_handler(self.resp, self.set_question)
            except ValueError:
                self.bot.send_message(self.user_id, "В аргументах должно быть число")
                self.bot.register_next_step_handler(self.resp, self.set_question)
        elif message.text.startswith("/end"):
            connection = sqlite3.connect('Games.db')
            cursor = connection.cursor()
            try:
                cursor.execute("delete from '{}' where 1 = 1".format(self.gamename))
                [cursor.execute("insert into '{}' values (?, ?)".format(self.gamename), i) for i in self.questions]
            except sqlite3.OperationalError:
                cursor.execute("""CREATE TABLE '{}' (
                                'question'	TEXT NOT NULL,
                                'answer'	TEXT NOT NULL);""".format(self.gamename))
                [cursor.execute("insert into '{}' values (?, ?)".format(self.gamename), i) for i in self.questions]
            self.de()
            self.bot.send_message(self.user_id, "Квест создан")
            cursor.close()
            connection.commit()
            connection.close()
        else:
            try:
                q, a = message.text.split("\n")
                a = a.lower()
                if a == "":
                    raise ValueError
                if self.ind == -1:
                    self.questions.append([q, a])
                else:
                    self.questions[self.ind] = [q, a]
                    self.ind = -1
            except ValueError:
                self.bot.send_message(self.user_id, "Неверный формат ввода вопроса. Попробуйте ещё раз.")
            self.bot.register_next_step_handler(self.resp, self.set_question)

    def results(self, message):
        connection = sqlite3.connect('Games.db')
        cursor = connection.cursor()
        try:
            teams = cursor.execute('select * from Teams').fetchall()
            for i in teams:
                name = str(i[0]) + "\n"
                games = i[2].split(",")
                points = i[3].split(',')
                try:
                    p = list(map(int, points))
                except ValueError:
                    p = [0]
                p = "\nИтого: " + str(sum(p))
                z = zip(games, points)
                z = "\n".join([" - ".join(list(i))+" баллов" for i in z])
                if z == " -  баллов":
                    z = "Пройденный квестов нет"
                self.bot.send_message(self.user_id, name+z+p)
        except:
            self.bot.send_message(self.user_id, "Результатов нет")

    list_commands = {
        "/создать_квест": set_game,
        '/добавить_участника': add_user,
        '/добавить_администратора': add_user,
        '/установить_расписание': set_schedule,
        '/расписание': get_schedule,
        '/сообщение': give_message,
        '/дать_ачивку': give_achievement,
        '/ачивки': achievement_list,
        '/результаты': results,
        '/имя': set_sth,
        '/фамилия': set_sth,
        '/отчество': set_sth,
        '/осебе': set_sth,
        '/номер': set_sth,
        '/деятельность': set_sth,
        '/где': whereis,
        '/руководители': users,
        '/участники': users
    }
