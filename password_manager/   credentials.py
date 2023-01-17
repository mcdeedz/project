from tkinter import *
import pyglet
from database import Database
from password_encryption import *

# Anzeigen der Zugangsdaten
class Credentials:

    def __init__(self, window):
        self.top = Toplevel(window)
        self.top.geometry("")
        self.top.title("Zugangsdaten")
        pyglet.font.add_file('DMSans.ttf')
        Label(self.top, text=f"Website", fg='black', font=('DMSans', '18', 'bold')).grid(column=0, row=2)
        Label(self.top, text=f"Username", fg='black', font=('DMSans', '18', 'bold')).grid(column=1, row=2)
        Label(self.top, text=f"Password", fg='black', font=('DMSans', '18', 'bold')).grid(column=2, row=2)
        Label(self.top, text=f"Search", fg='black', font=('DMSans', '18', 'bold')).grid(column=0, row=1)
        self.search_box = Entry(self.top, width=13, fg='black')
        self.search_box.grid(column=1, row=1)
        self.r = 3
        self.i = 0
        self.website_row = []
        self.username_row = []
        self.password_row = []
        self.decoded_pw = []
        self.website_entry_list = []
        self.username_entry_list = []
        self.password_entry_list = []
        self.database = Database()
        self.credentials = {}
        self.search_mode = 0

    def clipboard(self, pw):
        self.top.clipboard_clear()
        self.top.clipboard_append(pw)

    def delete_entries(self):
        for f1 in self.website_entry_list:
            f1.delete(0, END)

        for f2 in self.username_entry_list:
            f2.delete(0, END)

        for f3 in self.password_entry_list:
            f3.delete(0, END)

    def main_search(self):
        # Zugangsdaten aus der SQL DB importieren
        self.website_row = self.database.website_data()
        self.username_row = self.database.username_data()
        self.password_row = self.database.password_data()

        # Neuen Suchvorgang triggern
        Button(self.top, text="OK", command=self.another_search).grid(column=2, row=1)
        self.top.bind('<Return>', lambda event: self.another_search())

        # Zugangsdaten werden in GUI geladen
        for length in range(len(self.website_row)):
            entry = Entry(self.top, width=13, fg='black', font='DMSans')
            self.website_entry_list.append(entry)
            self.website_entry_list[self.i].grid(row=self.r, column=0)
            self.website_entry_list[self.i].insert(END, self.website_row[self.i])

            entry = Entry(self.top, width=13, fg='black', font='DMSans')
            self.username_entry_list.append(entry)
            self.username_entry_list[self.i].grid(row=self.r, column=1)
            self.username_entry_list[self.i].insert(END, self.username_row[self.i])

            entry = Entry(self.top, width=13, fg='black', font='DMSans')
            self.password_entry_list.append(entry)
            self.password_entry_list[self.i].grid(row=self.r, column=2)

            # Passwort entschlüsseln
            dec_pw = decrypt(self.password_row[self.i])
            self.password_entry_list[self.i].insert(END, dec_pw)
            self.i += 1
            self.r += 1

        self.i = 0
        self.r = 3

    def another_search(self):
        # Entry Lists löschen damit, sie wieder befüllt werden können.
        self.delete_entries()

        # Suchanfrage wird ausgeführt
        self.top.bind('<Return>', lambda event: self.another_search())

        self.website_row = self.database.website_data(import_mode=2, search_box=self.search_box.get())
        self.username_row = self.database.username_data(import_mode=2, searchbox=self.search_box.get())
        self.password_row = self.database.password_data(import_mode=2, searchbox=self.search_box.get())

        # Zugangsdaten werden in die bestehenden Entrys geschrieben
        for length in range(len(self.website_row)):
            self.website_entry_list[self.i].grid(row=self.r, column=0)
            self.website_entry_list[self.i].insert(END, self.website_row[self.i])

            self.username_entry_list[self.i].grid(row=self.r, column=1)
            self.username_entry_list[self.i].insert(END, self.username_row[self.i])

            self.password_entry_list[self.i].grid(row=self.r, column=2)
            # Password entschlüsseln
            dec_pw = decrypt(self.password_row[self.i])
            self.password_entry_list[self.i].insert(END, dec_pw)
            self.i += 1
            self.r += 1

        self.i = 0
        self.r = 3
