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
    
    def __init__(self, db):
        self.db_name = db
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_tables()

        self.all_data = {}

        self.cursor.execute("SELECT token FROM Accounts")
        tokens = self.cursor.fetchall()
        self.cursor.execute("SELECT password FROM Accounts")
        passwords = self.cursor.fetchall()
        self.cursor.execute("SELECT login FROM Accounts")
        logins = self.cursor.fetchall()
        
        for i in range(len(tokens)):
            self.all_data[logins[i][0]] = {"login": logins[i][0], "password": passwords[i][0], "token":tokens[i][0]}

    def create_account(self, username, password):
        usab = True
        print(self.all_data)
        for i in self.all_data:
            if i == username:
                print("Not usable username.")
                usab = False

        if usab:
            def generate_token(length=8):
                characters = string.ascii_letters + string.digits
                token = ''.join(random.choice(characters) for _ in range(length))

                return token
            token_gen = "TKN_"+generate_token()
            self.cursor.execute("INSERT INTO Accounts(login, password, token) values(?, ?, ?)",
                                [username, password, token_gen])
            self.cursor.execute("CREATE TABLE "+token_gen+" ( done INTEGER, text TEXT NOT NULL, id INTEGER PRIMARY KEY)")
            self.db.commit()
        self.__init__(self.db_name)


    def drop_all(self):
        self.cursor.execute('''SELECT * FROM Accounts''')
        records = self.cursor.fetchall()
        print(records)
        for item in records:
            self.cursor.execute("DROP TABLE "+item[2])
        self.cursor.execute("DROP TABLE Accounts")
        self.__init__(self.db_name)

    def get_password(self, login=str):
        return self.all_data[login]["password"]
    def get_token(self, login=str):
        return self.all_data[login]["token"]
    def drop_table(self, table=str):
        self.cursor.execute("DROP TABLE " + table)
        self.db.commit()
        
if __name__ == "__main__":
    db = account_manager("Accounts.db")
    db.create_account("Kyu", "legit me")