from threading import Thread

from flask import Flask, render_template, request, make_response

from SQLManager import SQLManaging
from account_managing import account_manager

app = Flask(__name__)

acc_db_iter = account_manager("Accounts.db")
test_database = SQLManaging("todolist.db", "Todo_list")
todolist = test_database.get_info()


@app.route("/")
def index():
    if request.cookies and "token" in request.cookies and "token" != "":
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route("/api/get")
def get():
    global todolist
    token = request.headers.get("token")

    if acc_db_iter.validate_token(token):
        todolist = SQLManaging("Accounts.db", token).get_info()
        return make_response(todolist, 200)
    else:
        return make_response("Unknown user", 401)


@app.route("/api/update", methods=["POST"])
def update():
    global todolist
    token = request.headers.get("token")

    if acc_db_iter.validate_token(token):
        todolist = request.json
        SQLManaging("Accounts.db", token).update(todolist)
        return make_response(todolist, 200)
    else:
        return make_response("Unknown user", 401)


@app.route("/account/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    if username in acc_db_iter.users:
        if acc_db_iter.all_data[username]["password"] == password:
            return make_response(acc_db_iter.all_data[username]["token"], 200)
        else:
            return make_response("Incorrect password", 401)
    else:
        return make_response("Unknown user", 401)


@app.route("/account/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    print(username)
    print(password)
    users = []
    for i in acc_db_iter.all_data:
        users.append(i)

    if username in users:
        return make_response("Username already taken", 401)
    else:
        acc_db_iter.create_account(username, password)
        return make_response(acc_db_iter.all_data[username]["token"], 200)


@app.route("/account/username", methods=["GET"])
def get_username():
    token = request.headers.get("token")
    print(token)

    if token == "testtoken":
        return make_response("test", 200)
    else:
        if acc_db_iter.validate_token(token):
            return make_response(acc_db_iter.get_username(token), 200)
        else:
            return make_response("Unknown user", 401)


def run():
    app.run(host="0.0.0.0", port=5000)


def start():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    start()
