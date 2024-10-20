from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2,  4)
    nr_numbers = random.randint(2, 4)

    new_letters = [random.choice(letters) for letter in range(nr_letters)]

    new_symbols = [random.choice(symbols) for symbol in range(nr_symbols)]

    new_numbers = [random.choice(numbers) for number in range(nr_numbers)]

    password_list = new_letters + new_symbols + new_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    pasentry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = webentry.get()
    email = emusentry.get()
    password = pasentry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nemail: {email}\npassword: {password}\nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    #reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                #updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    #saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                webentry.delete(0, 'end')
                pasentry.delete(0, 'end')

def find_password():

    website = webentry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"email: {data[website]['email']}\npassword: {data[website]['password']}")
        else:
            messagebox.showinfo(title="oops", message=f"No details for {website} exist")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("password manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200)
pic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pic)
canvas.grid(row=0, column=1)

web = Label(text="Website:")
web.grid(row=1, column=0)

emus = Label(text="Email/Username:")
emus.grid(row=2, column=0)

pas = Label(text="Password:")
pas.grid(row=3, column=0)

webentry = Entry(width=40)
webentry.grid(row=1, column=1, columnspan=2, sticky="e")
webentry.focus()

emusentry = Entry(width=40)
emusentry.grid(row=2, column=1, columnspan=2, sticky="e")
emusentry.insert(0, "elena@gmail.com")

pasentry = Entry(width=22)
pasentry.grid(row=3, column=1, sticky="e")

genpas = Button(text="Generate Password", command=generate_password)
genpas.grid(row=3, column=2, sticky="w")

add = Button(text="Add", width=34, command=save)
add.grid(row=4, column=1, columnspan=2, sticky="e")

search = Button(text="Search", width=14, command=find_password)
search.grid(row=1, column=2, sticky="e")

window.mainloop()
