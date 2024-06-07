from threading import Thread

from flask import Flask, render_template, request, make_response

from SQLManager import SQLManaging
from account_managing import account_manager

app = Flask(__name__)

acc_database = account_manager("Accounts.db")
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
    print(token)

    tokens = []
    for i in acc_database.all_data:
        tokens.append(acc_database.all_data[i]["token"])

    # _TODO: Add a case for if the token is not in the database
    # acc_database.create_token_table(token)
    if token == "testtoken":
        todolist = test_database.get_info()
        print(todolist)
        return make_response(todolist, 200)
    else:
        if token not in tokens:
            return make_response("Unknown user", 401)
        else:
            todolist = SQLManaging("Accounts.db", token).get_info()
            print(todolist)
            return make_response(todolist, 200)


@app.route("/api/update", methods=["POST"])
def update():
    global todolist

    token = request.headers.get("token")
    print(token)
    print(todolist)

    tokens = []
    for i in acc_database.all_data:
        tokens.append(acc_database.all_data[i]["token"])

    # _TODO (DONE): Add a case for if the token is not in the database

    if token == "testtoken":
        todolist = request.json
        test_database.update(todolist)
        print(todolist)
        return make_response(todolist, 200)

    else:
        if token not in tokens:
            return make_response("Unknown user", 401)
        else:
            todolist = request.json
            SQLManaging("Accounts.db", token).update(todolist)
            print(todolist)
            return make_response(todolist, 200)


@app.route("/account/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    print(username)
    print(password)

    if username in acc_database.users:
        if acc_database.all_data[username]["password"] == password:
            return make_response(acc_database.all_data[username]["token"], 200)
        else:
            return make_response("Incorrect password", 401)
    elif username == "test":
        if password == "test":
            return make_response("testtoken", 200)
        else:
            return make_response("Wrong password", 401)
    else:
        return make_response("Unknown user", 401)


@app.route("/account/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    print(username)
    print(password)
    users = []
    for i in acc_database.all_data:
        users.append(i)

    if username in users:
        return make_response("Username already taken", 401)
    else:
        acc_database.create_account(username, password)
        return make_response(acc_database.all_data[username]["token"], 200)


@app.route("/account/username", methods=["GET"])
def get_username():
    token = request.headers.get("token")

    # _TODO (DONE): Backend logic
    # _TODO (DONE: Add a case for if the token is not in the database

    #! from kyu: added the token table creation if the account exists but the table for it doesnt <3

    tokens = []
    for i in acc_database.all_data:
        tokens.append(acc_database.all_data[i]["token"])

    if token == "testtoken":
        return make_response("test", 200)
    else:
        if token in tokens:
            return make_response(acc_database.get_username(token), 200)
        else:
            return make_response("Unknown user", 401)


def run():
    app.run(host="0.0.0.0", port=5000)


def start():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    start()
