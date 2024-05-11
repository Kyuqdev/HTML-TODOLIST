import sqlite3
class SQLManaging():
    def __init__(self, db):
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cr = self.db.cursor()
        #the main db


    def create_tables(self):
        #creates basic tables for the todo list
        self.cr.execute('''
                            CREATE TABLE IF NOT EXISTS Todo_list (
                            done INTEGER,
                            text TEXT NOT NULL
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
            records_formated.append({"text":records[i-1][1], "done":done})
        return records_formated
    def create_part(self, done=False, textt=str):
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
            self.cr.execute('''INSERT INTO Todo_list(done, text) values(?, ?)''', [new_info[i-1]["done"],new_info[i-1]["text"]])
        self.db.commit()

db = SQLManaging("todolist.db")
db.create_tables()
#TODO get real