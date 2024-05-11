from threading import Thread
import flask
from flask import Flask, render_template, request
from SQLManager import SQLManaging


app = Flask(__name__)

database = SQLManaging("todolist.db")
todolist = database.get_info()
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api/get")
def get():
    return todolist, "just in case yo dumbass god the code fucked up here is the thing"

@app.route("/api/update", methods=["POST"])
def update():
    global todolist

    todolist = request.json
    #database.update(todolist)
    print(todolist)
    return todolist

def run():
    app.run(host="0.0.0.0", port=5000)

def start():
    t =Thread(target=run)
    t.start()
    
if __name__ == "__main__":
    start()