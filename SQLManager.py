import sqlite3


class SQLManaging:
    def __init__(self, db, table):
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.table = table
        self.cr = self.db.cursor()
        #? ill make this class for managing the user tables
        self.create_table()
    def create_table(self):
        self.cr.execute("CREATE TABLE IF NOT EXISTS "+self.table+"(done INTEGER, text TEXT NOT NULL, id INTEGER PRIMARY KEY)")
        self.db.commit()
    def get_info(self):
        self.cr.execute(
            f"""
                            SELECT * FROM {self.table};
                            """
        )
        records = self.cr.fetchall()
        records_formated = []
        for record in records:
            if record[0] == 1:
                done = True
            else:
                done = False
            records_formated.append(
                {"text": record[1], "done": done, "id": record[2]}
            )
        if len(records_formated) !=0:
            return records_formated
        else:
            return []
    def create_part(self, textt, done=False):
        self.cr.execute(
            f"""INSERT INTO {self.table}(done, text) values(?,?)""", [done, textt]
        )
        self.db.commit()
    def execute_that(self, command):
        self.cr.execute(command)
        self.db.commit()
    def update(self, new_info):
        self.cr.execute(f"""DROP TABLE {self.table};""")
        self.db.commit()
        self.create_table()
        for item in new_info:
            self.cr.execute(
                f"""INSERT INTO {self.table}(done, text) values(?, ?)""",
                [
                    item["done"],
                    item["text"]
                ],
            )
        self.db.commit()

    #!next functions arent really useful i just left them in case of maintanance

    def execute_func(self):
        function_list = ["create tables", "get info", "create part", "drop table"]
        which = input(("which function?" + str(function_list)))

        while which not in function_list:
            which = input("not in list or bad pronounc., which function?")
        if which == "create tables":
            self.create_table()
        elif which == "get info":
            print(self.get_info())
        elif which == "create part":
            self.create_part(textt=input("text"), done=int(input("Done or not? (1 or 0)")))

        self.db.commit()
print(__name__)
if __name__ == "__main__":
    db = SQLManaging("todolist.db", input("What table token to enter?"))
    #function to execute other function inside of SQLManaging class used for debugging preferebly comment it
    db.execute_func()