import sqlite3
import random
import string
class account_manager():
    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts (
                                login TEXT NOT NULL,
                                password TEXT NOT NULL,
                                token TEXT NOT NULL
                                )""")
        self.db.commit()
    def read_info(self):

        self.cursor.execute("SELECT token FROM Accounts")
        tokens = self.cursor.fetchall()
        self.cursor.execute("SELECT password FROM Accounts")
        passwords = self.cursor.fetchall()
        self.cursor.execute("SELECT login FROM Accounts")
        logins = self.cursor.fetchall()

        for i in range(len(tokens)):
            self.all_data[logins[i][0]] = {"login": logins[i][0], "password": passwords[i][0], "token": tokens[i][0]}

        for i in self.all_data:
            self.users.append(i)
    def __init__(self, db):
        self.db_name = db
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_tables()
        self.all_data = {}
        self.users = []
        self.read_info()
    def create_token_table(self, t):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + t + " ( done INTEGER, text TEXT NOT NULL, id INTEGER PRIMARY KEY)")
        self.db.commit()

    def create_account(self, username, password):
        usable = True
        self.read_info()
        for item in self.all_data:
            if item == username:
                print("Not usable username.")
                usable = False

        if usable:
            def generate_token(length=8):
                characters = string.ascii_letters + string.digits
                token = ''.join(random.choice(characters) for _ in range(length))

                return "TKN_"+token
            token_gen = generate_token()
            self.cursor.execute("INSERT INTO Accounts(login, password, token) values(?, ?, ?)",
                                [username, password, token_gen])
            self.create_token_table(token_gen)
        self.read_info()
    def drop_all(self):
        self.__init__(self.db_name)
        for item in self.all_data:
            self.cursor.execute("DROP TABLE "+self.all_data[item]["token"])
        self.cursor.execute("DROP TABLE Accounts")
        self.__init__(self.db_name)
    def get_password(self, login=str):
        return self.all_data[login]["password"]
    def get_token(self, login=str):
        return self.all_data[login]["token"]
    def get_username(self, token):
        for i in self.all_data:
            if token == self.all_data[i]["token"]:
                return self.all_data[i]["login"]

    def drop_table(self, table=str):
        self.cursor.execute("DROP TABLE " + table)
        self.db.commit()
    def execute(self):
        strin=''
        commands = [
            "create tables",
            "read info",
            "init",
            "create account",
            "drop all",
            "get password",
            "get token",
            "drop table"]
        for i in commands:
            strin +="\n"+i
        command = input(f"""What command to execute?{strin}""")
        while command not in commands:
            command = input(f"""Invalid command. What command to execute?\n {strin}""")
        if command == "drop all":
            self.drop_all()
        if command == "create account":
            self.create_account(input("Username:"), input("Password"))
        if command == "init":
            self.__init__(self.db_name)


if __name__ == "__main__":
    db = account_manager("Accounts.db")
    db.execute()
