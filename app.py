import BackEnd
from flask import Flask, session, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    tmp1, tmp2 = BackEnd.get_chatlog()
    session['lastmsg'] = tmp2
    return render_template("index.html",
                           chat=tmp1)


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
    lastmsg = session['lastmsg']
    string, lastmsg = BackEnd.get_chatlog_lastfrom(lastmsg)
    if string == 0:
        return jsonify(nsfw='KOK')
    session['lastmsg'] = lastmsg

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


@app.route("/_logout")
def logout():
    print('logout')
    if 'username' in session:
        print('+')
        session.pop('username', None)
        return jsonify()


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
@app.route("/_isLogged")
def isLogged():
    print('Login check')
    if 'username' in session:
        print('User is Logged')
        return jsonify(nsfw=1)
    else:
        print('User is NOT logged')
        return jsonify(nsfw=0)


# set the secret key.  keep this really secret:
app.secret_key = 'Secret Key! SO SECRET!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
