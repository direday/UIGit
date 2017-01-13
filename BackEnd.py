import sqlite3

# path = 'D:/Dropbox/Programming/Python/UIGit/static/db/Data.db'

path = 'C:/Files/Dropbox/Programming/Python/UIGit/static/db/Data.db'

# path = 'E:/Study/Server/static/db/Data.db'

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

    return strings


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
    print('send:<', msg, '>')

    db = sqlite3.connect(path)
    c = db.cursor()
    strings = []
    c.execute("select * from chat order by id desc")
    row = c.fetchone()
    for i in range(0, n):
        # print('row2:<', row[2], '>')
        if row == None:
            break
        if row[2] == msg:
            break
        strings.append(row[1] + ': ' + row[2] + '\n')
        row = c.fetchone()

    strings.reverse()
    lastmsg = strings[len(strings)-1]
    str = ''
    for i in range(0, len(strings)):
        str += strings[i]
    # print(str)
    return str, lastmsg
