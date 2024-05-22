from threading import Thread
import flask
from flask import Flask, render_template, request, make_response
from SQLManager import SQLManaging


app = Flask(__name__)

database = SQLManaging("todolist.db")
todolist = database.get_info()


@app.route("/")
def index():
    if request.cookies and "token" in request.cookies:
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route("/api/get")
def get():
    token = request.headers.get("token")
    print(token)

    if token != "testtoken":
        return make_response("Unauthorized", 401)

    else:
        todolist = database.get_info()
        print(todolist)
        return make_response(todolist, 200)


@app.route("/api/update", methods=["POST"])
def update():
    global todolist

    token = request.headers.get("token")
    print(token)
    print(todolist)

    if token != "testtoken":
        return make_response("Unauthorized", 401)

    else:
        todolist = request.json
        database.update(todolist)
        print(todolist)
        return make_response(todolist, 200)


@app.route("/account/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    if username == "test":
        if password == "test":
            return make_response("testtoken", 200)
        return make_response("Wrong password", 401)
    else:
        return make_response("Unknown user", 401)


def run():
    app.run(host="0.0.0.0", port=5000)


def start():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    start()
