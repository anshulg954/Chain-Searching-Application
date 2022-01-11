import tkinter as tk
from tkinter import *
from tkinter import messagebox
from simple_search import search_app


def query(chain):
    if(chain == ""):
        # error notificaion
        messagebox.showinfo('Error', 'Please fill some data!')
    else:
        ans = search_app(chain)
        # data saved notification
        if(len(ans) > 0):
            messagebox.showinfo(
                'Success', 'Data has been saved in: ./outputs/'+chain+'.json\nThe number of entries found are:'+str(len(ans)))
        else:
            messagebox.showinfo(
                'Oops', 'No data found!!\nThe number of entries found are:'+str(len(ans)))


root = tk.Tk()

root.title("RCSB Chain Finder")
window_width = 500
window_height = 300
root.geometry("500x300")

# window allignment
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width,
                                   window_height, x_cordinate, y_cordinate))

label_0 = Label(root, text="Chain Searching", width=20, font=("bold", 20))
label_0.place(x=90, y=60)


# this creates 'Label' widget for Fullname and uses place() method.
label1 = Label(root, text="Sub-chain", width=20, font=("bold", 10))
label1.place(x=80, y=130)

# this will accept the input string text from the user.
entry = Entry(root)
entry.place(x=240, y=130)

# submit button
Button(root, text='Submit', width=20, bg="black",
       fg='white', command=lambda: query(entry.get())).place(x=180, y=200)

root.mainloop()
