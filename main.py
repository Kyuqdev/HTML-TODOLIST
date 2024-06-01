from threading import Thread
import flask
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
    token = request.headers.get("token")
    print(token)

    # TODO: Add a case for if the token is not in the database
    if token == "testtoken":
        todolist = test_database.get_info()
        print(todolist)
        return make_response(todolist, 200)
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

    # TODO: Add a case for if the token is not in the database
    if token == "testtoken":
        todolist = request.json
        test_database.update(todolist)
        print(todolist)
        return make_response(todolist, 200)

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

    if acc_database.all_data[username]["password"] == password:
        return make_response(acc_database.all_data[username]["token"], 200)
    elif username == "test":
        if password == "test":
            return make_response("testtoken", 200)
        return make_response("Wrong password", 401)
    else:
        return make_response("Unknown user", 401)


@app.route("/account/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    print(username)
    print(password)

    # TODO: backend logic for account creation

    if username in []:
        return make_response("Username already taken", 401)
    else:
        # ? create account here
        return make_response("Account created", 200)


@app.route("/account/username", methods=["GET"])
def get_username():
    token = request.headers.get("token")

    # TODO: Backend logic
    # TODO: Add a case for if the token is not in the database
    if token == "testtoken":
        return make_response("test", 200)
    else:
        return make_response("Unknown user", 401)


def run():
    app.run(host="0.0.0.0", port=5000)


def start():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    start()
#!im cumming vro
