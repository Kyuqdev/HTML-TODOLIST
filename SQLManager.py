import sqlite3
class SQLManaging():
    def __init__(self, db):
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cr = self.db.cursor()
        #the main db


    def create_tables(self):
        #creates basic tables for the todo list
        #this is a test comment
        self.cr.execute('''
                            CREATE TABLE IF NOT EXISTS Todo_list (
                            done INTEGER,
                            text TEXT NOT NULL,
                            id INTEGER PRIMARY KEY
                            )
                            ''')
        self.db.commit()
    
    def get_info(self):
        self.cr.execute('''
                            SELECT * FROM Todo_list;
                            ''')
        records = self.cr.fetchall()
        records_formated = []
        for i in range(len(records)):
            if records[i-1][0] == 1:
                done = True
            else:
                done = False
            records_formated.append({"text":records[i-1][1], "done":done, "id":records[i-1][2]})
        return records_formated
    def create_part(self, textt=str, done=False):
        self.cr.execute('''INSERT INTO Todo_list(done, text) values(?,?)''', [done, textt])
        self.db.commit()

    def execute_that(self, command):
        self.cr.execute(command)
        self.db.commit()
    
    def update(self, new_info):
        self.cr.execute('''DROP TABLE Todo_list;''')
        self.db.commit()
        self.create_tables()
        for i in range(len(new_info)):
            self.cr.execute('''INSERT INTO Todo_list(done, text, id) values(?, ?, ?)''', [new_info[i-1]["done"],new_info[i-1]["text"], new_info[i-1]["id"]])
        self.db.commit()
    def drop_table(self, table=str):
        self.cr.execute('DROP TABLE '+table)
        self.db.commit()
    def execute_func(self):
        function_list = ["create tables", "get info", "create part", "drop table"]
        which = input(("which function?"+ str(function_list)))


        while which not in function_list:
            which = input("not in list or bad pronounc., which function?")
        if which == "create tables":
            self.create_tables()
        elif which == "get info":
            print(self.get_info())
        elif which == "create part":
            self.create_part(textt=input("text"), done=int(input("Done or not? (1 or 0)")))
        elif which == "drop table":
            self.drop_table(input("Which table?(current tables: Todo_list)"))

db = SQLManaging("todolist.db")
#function to execute other function inside of SQLManaging class used for debugging preferebly comment it
#db.execute_func()
#TODO get real