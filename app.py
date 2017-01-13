import BackEnd
from flask import Flask, session, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    tmp = BackEnd.get_chatlog()
    tmp2 = tmp[len(tmp)-1]
    tmp3 = ''
    for i in range(0, len(tmp2)-2):
        if (tmp2[i] == ':') and (tmp2[i+1] == ' '):
            tmp3 += tmp2[i+2:-1]
    session['lastmsg'] = tmp3

    return render_template("index.html",
                           chat=tmp)


# Отправка сообщения в чат и добавление его в бд
@app.route("/_sendMessage")
def sendMessage():
    msg = request.args.get('msg', 0, type=str)
    if 'username' not in session:
        return jsonify()
    username = session['username']
    BackEnd.send_message(username, msg)

    return jsonify()


# Обновление чата. (Принимает последнее отображаемое в чате сообщение, а
#  отправляет строку содержащую все сообщение отправленные после данного)
@app.route("/_updtChat")
def uptdChat():
    print('update!')
    tmp2 = session['lastmsg']
    string, tmp = BackEnd.get_chatlog_lastfrom(tmp2)
    tmp2 = ''
    for i in range(0, len(tmp)-2):
        if (tmp[i] == ':') and (tmp[i+1] == ' '):
            tmp2 += tmp[i+2:-1]
    session['lastmsg'] = tmp2
    return jsonify(nsfw=string)


# Вход на сервер
@app.route("/_tryLogin")
def tryLogin():
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0, type=str)
    tmp = BackEnd.sign_in(login, password)
    if tmp == 'SUCC':
        session['username'] = login
    return jsonify(nsfw=tmp)


# Регистрация на сервере
@app.route('/_register')
def register():
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0, type=str)
    tmp = BackEnd.add_user(login, password)
    if tmp == 'SUCC':
        session['username'] = login
    return jsonify(nsfw=tmp)


# Запрос на проверку залогинен ли пользователь
@app.route("/_logged")
def logged():
    if 'username' in session:
        return jsonify(nsfw=1)
    else:
        return jsonify(nsfw=0)


# Выход с сервера
@app.route('/_logout')
def logout():
    session.pop('username', None)


# set the secret key.  keep this really secret:
app.secret_key = 'Secret Key! SO SECRET!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
