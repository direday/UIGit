import sqlite3
import os

# Путь к базе данных
path = os.getcwd() + "\static\db\Data.db"

# Регистрация пользователя
def add_user(userlogin, userpassword):
    db = sqlite3.connect(path)
    c = db.cursor()

    # Проверка на уникальность логина
    c.execute("select count (*) from users where login=:ul", {"ul": userlogin})
    t = c.fetchone()
    if t[0] != 0:
        print('Уже есть такой, не добалено.')
        return 'LOG'

    data = (userlogin, userpassword)

    # Добавление записи в базу данных
    c.execute("INSERT INTO users (login,password) VALUES (?,?)", data)
    db.commit()
    return 'SUCC'


# Проверка входа
def sign_in(login, password):
    db = sqlite3.connect(path)
    c = db.cursor()

    c.execute("select count (*) from users where login=:lg", {"lg": login})
    t = c.fetchone()
    if t[0] == 0:
        print('Неправильно указан логин.')
        return 'LOG'
    c.execute("select * from users where login=:lg", {"lg": login})
    raw = c.fetchone()
    if password != raw[2]:
        print("Неправильный пароль!")
        return 'PASS'
    if password == raw[2]:
        print("Всё правильно!")
        return 'SUCC'


# Отправка сообщения
def send_message(username, message):
    db = sqlite3.connect(path)
    c = db.cursor()

    data = (username, message)
    c.execute("INSERT INTO chat (author,message) VALUES (?,?)", data)
    db.commit()


# Запрос всех сообщений чата
def get_chatlog():
    db = sqlite3.connect(path)
    c = db.cursor()

    strings = []
    c.execute("select * from chat order by id asc")
    for i in c:
        # print(i[1] + ': ' + i[2])
        strings.append(i[1] + ': ' + i[2] + '\n')
        lastmsg = int(i[0])

    return strings, lastmsg


# Запрос последних n сообщений чата
def get_chatlog_lastN():
    n = 10

    db = sqlite3.connect(path)
    c = db.cursor()
    strings = []
    c.execute("select * from chat order by id desc")
    row = c.fetchone()
    for i in range(0, n):
        if row == None:
            break
        strings.append(row[1] + ': ' + row[2] + '\n')
        row = c.fetchone()

    strings.reverse()
    return strings


# Запрос сообщений чата после данного
def get_chatlog_lastfrom(msg):
    n = 10

    db = sqlite3.connect(path)
    c = db.cursor()
    strings = []
    c.execute("select * from chat order by id desc")
    row = c.fetchone()
    lastmsg = int(row[0])
    # if lastmsg == msg:
    #     return 0, msg
    for i in range(0, n):
        if row == None:
            break
        if int(row[0]) == msg:
            break
        strings.append(row[1] + ': ' + row[2] + '\n')
        row = c.fetchone()

    strings.reverse()
    if len(strings) != 0:
        return strings, lastmsg
    else:
        return 0, msg
