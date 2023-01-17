import sqlite3
import pandas


# TODO:15. Ziel ist es der Class Credentials nur die Website, Username, Password als Listen mit Dicts zu übergeben
#  Die Daten werden in der Class Database vollständig importiert, verarbeitet und dann an  Class Credentials übergeben
#  In Credentials wird nur zb. self.Website ausgerufen und die Daten übergeben.
#
#  **************.
class Database:
    def __init__(self):
        self.connection = sqlite3.connect("pw.db")
        self.credential_db = self.connection.cursor()
        self.website_row = []
        self.username_row = []
        self.password_row = []

    def insert(self, query):
        self.credential_db.execute('''insert into credentials (website, username, password) values (?, ?, ?)''', query)
        self.connection.commit()

    def delete(self):
        self.credential_db.execute('''delete from credentials;''')
        self.connection.commit()

    def import_data(self, search_box="", import_mode=1):
        if import_mode == 1:
            self.credential_db.execute("SELECT website, username, password FROM credentials")
            self.connection.commit()
            return pandas.DataFrame(self.credential_db.fetchall(),
                                    columns=['website', 'username', 'password']).to_dict()

        elif import_mode == 2:
            self.credential_db.execute("SELECT website, username, password FROM credentials"
                                       " WHERE website like ? OR username like ?",
                                       ('%' + search_box + '%', '%' + search_box + '%'))
            self.connection.commit()
            return pandas.DataFrame(self.credential_db.fetchall(),
                                    columns=['website', 'username', 'password']).to_dict()

    def website_data(self, search_box="", import_mode=1):
        if import_mode == 1:
            imported = self.import_data()
            self.website_row = imported["website"]
            return self.website_row
        elif import_mode == 2:
            imported = self.import_data(search_box=search_box, import_mode=import_mode)
            self.website_row = imported["website"]
            return self.website_row

    def username_data(self, searchbox="", import_mode=1):
        if import_mode == 1:
            imported = self.import_data()
            self.username_row = imported["username"]
            return self.username_row
        elif import_mode == 2:
            imported = self.import_data(search_box=searchbox, import_mode=import_mode)
            self.username_row = imported["username"]
            return self.username_row

    def password_data(self, searchbox="", import_mode=1):
        if import_mode == 1:
            imported = self.import_data()
            self.password_row = imported["password"]
            return self.password_row
        elif import_mode == 2:
            imported = self.import_data(search_box=searchbox, import_mode=import_mode)
            self.password_row = imported["password"]
            return self.password_row
