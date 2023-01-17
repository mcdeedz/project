from tkinter import *
from credentials import *
import pyglet
from pw_generator import *
from password_encryption import *
from database import *


# TODO:1. ###DONE### Passwort mit Base64 Kodierung in die SQL Datenbank speichern.
# TODO:2. ###DONE### Passwort dekodieren->Funktion erstellt.
# TODO:3, Context Menü erstellen um Password, entschlüsselt zu kopieren.--->Noch sinnvoll? Siehe TODO 7.
# TODO:4. ###DONE### Password Abfrage für Zugangsdaten
# TODO:5. ###DONE### Password Falsch Meldung lässt sich nicht mit Enter schließen

# TODO:6. ###PRIO1###: In credentials.py, die Zugangsdaten in ein Pandas Dataframe laden und jede Tabellen Spalte einzeln ausgeben,
#         um Daten jeder Spalte handhaben zu können. https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/

# TODO:7. ###PRIO2### Nachdem TODO 6 erledigt, die Passwörter in credentials maskieren und einen PW kopieren Button implementieren
#         der die PWs entschlüsselt.

# TODO:8. ###PRIO3###: Statt Base64 Kodierung, Passwörter mit einer RSA verschlüsselung in der SQL Datenbank hinterlegen.
#  https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/

# TODO:9. ###DONE### Code aufteilen ?
# TODO 11. _tkinter.TclError: bad window path name ".!toplevel2.!entry2"
# TODO 13: ###DONE###  Andere Schleife verwenden!! iterrows erstell eine Kopie der Objekte her!!!
# TODO:14. ###DONE### Show Password Button im Hauptfenster
# TODO:15. ###DONE### Es ist mglw. sinnvoller das auslesen der Datenbank und die Weiterverarbeitung der Daten in eine eigene Klasse auszulagern
#  Eine Klasse für das Auslesen der Daten und eine für die Darstellung im Fenster.
# TODO:16. ###TODO 1###: Password Encryption Class erstellen.


def get_password_input():
    password = password_var.get()
    return password


def get_username_input():
    username = username_var.get()
    return username


def get_website_input():
    website = website_var.get()
    return website


def new_password():
    pw = Password()
    generated_password = pw.generate_password()
    window.clipboard_clear()
    window.clipboard_append(generated_password)
    password_input_field.delete('0', END)
    password_input_field.insert(END, generated_password)


def destroy_password_request_window(top_window):
    top_window.destroy()
    password_request_window()


def wrong_password_window():
    top3 = Toplevel(window)
    top3.geometry("400x100")
    top3.title("Passwort falsch!")
    Label(top3, text="Passwort falsch, versuche es nochmal!", font='DMSans').place(x=110, y=25)
    top3.bind('<Return>', lambda event: destroy_password_request_window(top3))
    Button(top3, text="OK", command=lambda: destroy_password_request_window(top3), font=('DMSans', '18', 'bold')).place(
        x=250, y=50)


def password_request_window():
    top2 = Toplevel(window)
    top2.geometry("400x90")
    top2.title("Bitte Passwort eingeben")
    top2.config(bg="white")
    top2.bind('<Return>', lambda event: credential_window_password_check(p_var.get(), top2))

    # email/username
    pw_label = Label(top2, text="Passwort:", bg="white", font=('DMSans', '18', 'bold'), borderwidth="5")
    pw_label.grid(column=1, row=4)

    p_var = StringVar()
    pw_label_text = Entry(top2, highlightbackground="white", textvariable=p_var, show="*")
    pw_label_text.grid(column=2, row=4)

    a_button = Button(top2, text="OK", height=1, width=15,
                      command=lambda: credential_window_password_check(p_var.get(), top2),
                      bg="white",
                      highlightbackground="white",
                      font=('DMSans', '18', 'bold'))
    a_button.grid(column=2, row=5)


def credential_window_password_check(password, window):
    if password == "Costumfis8!":
        window.destroy()
        open_credential_window()
    else:
        window.destroy()
        wrong_password_window()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_credentials(website, username, password):
    print(f"website:{website}, username:{username}, password:{password}")
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        empty_fields_window()
    else:
        save_password_window(website, username, password)


# ---------------------------- POPUP Windows ------------------------------- #

def empty_fields_window():
    top = Toplevel(window)
    top.geometry("500x200")
    top.title("Felder leer gelassen")
    Label(top, text="Bitte alle Felder ausfüllen!", font='DMSans').place(x=110, y=25)
    Button(top, text="OK", command=top.destroy, font=('DMSans', '18', 'bold')).place(x=250, y=50)


def save_password_window(website, username, password):
    pyglet.font.add_file('DMSans.ttf')
    top = Toplevel(window)
    top.geometry("500x150")
    top.title("Zugangsdaten")

    Label(top,text=f"Zugangsdaten erfolgreich gespeichert\nWebsite: {website}\nE-Mail: {username}\nPasswort: "
               f"{password}", font=('DMSans', '18', 'bold')).place(x=110, y=25)
    Button(top, text="OK", command=top.destroy, font=('DMSans', '18', 'bold')).place(x=200, y=110)

    # Zugangsdaten in der Datenbank abspeichern
    db_connection = Database()
    db_connection.insert((website, username, encrypt(password)))

    #  Lösche Zugangsdaten von den Eingabefeldern im Hauptfenster
    website_var.set("")
    username_var.set("")
    password_input_field.delete(0, END)


# ---------------------------- ZUGANGSDATEN ANZEIGEN ------------------------------- #

def open_credential_window():
    credential_search = Credentials(window)
    credential_search.main_search()


# ---------------------------- UI SETUP ------------------------------- #

# Fenster erzeugen
window = Tk()
window.title("Password Manager")
window.config(width=100, height=100, bg="white")

# Logo anzeigen

logo_img = PhotoImage(file="logo_cmagdits_300.png")
canvas = Canvas(width=300, height=130, bg="white", highlightbackground="white")
canvas.create_image(150, 70, image=logo_img)  #
canvas.grid(column=2, row=0)

# website
website_label = Label(text="Website:", bg="white", font=('DMSans', '18', 'bold'), borderwidth="5")
website_label.grid(column=1, row=2)

website_var = StringVar()
website_input_field = Entry(textvariable=website_var, highlightbackground="white")
website_input_field.grid(column=2, row=2)

# email/username
email_username_label = Label(text="Benutzername:", bg="white", highlightbackground="white",
                             font=('DMSans', '18', 'bold'), borderwidth="5")
email_username_label.grid(column=1, row=3)

username_var = StringVar()
username_input_field = Entry(textvariable=username_var, highlightbackground="white")
username_input_field.grid(column=2, row=3)

# email/username
credential_button = Button(text="Zugangsdaten anzeigen", command=lambda: password_request_window(), bg="white",
                           highlightbackground="white", font=('DMSans', '18', 'bold'), width=15)
credential_button.grid(column=3, row=3)

# Password
password_label = Label(text="Passwort:", bg="white", font=('DMSans', '18', 'bold'), borderwidth="5")
password_label.grid(column=1, row=4)

password_var = StringVar()
# show="*",
password_input_field = Entry(highlightbackground="white", textvariable=password_var)
password_input_field.grid(column=2, row=4)

# Generate Password
generate_password_button = Button(text="Password generieren", command=new_password, bg="white",
                                  highlightbackground="white",
                                  font=('DMSans', '18', 'bold'))
generate_password_button.grid(column=3, row=4)

# Add
add_password_button = Button(text="Hinzufügen", height=1, width=15,
                             command=lambda: add_credentials(website=get_website_input(), username=get_username_input(),
                                                             password=get_password_input()), bg="white",
                             highlightbackground="white",
                             font=('DMSans', '18', 'bold'))
add_password_button.grid(column=2, row=5)

window.mainloop()
