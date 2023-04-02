from tkinter import *
from random import randint
from PIL import ImageTk, Image
import os

# automatically create list of pictures in food_pics
food_pics = [file for file in os.listdir("food_pics")]
# print(food_pics)

root = Tk()
root.geometry("700x500")

# create a frame to display pictures
imgFrame = Frame(root, width=600, height=400)
imgFrame.pack()
imgFrame.place(anchor='center', relx=0.5, rely=0.4)

original = Image.open('food_pics/' + food_pics[0])
img = ImageTk.PhotoImage(original.resize((300, 400), Image.ANTIALIAS))
label = Label(imgFrame, image=img)
label.pack()

# create a frame to display choices
choiceFrame = Frame(root, width=600, height=100)
choiceFrame.pack(side=BOTTOM)
choiceFrame.place(anchor='center', relx=0.5, rely=0.9)

choice1 = Label(choiceFrame, text="Choice 1", padx=20, font=('Helvetica', 30))
choice1.grid(row=0, column=0)
choice2 = Label(choiceFrame, text="Choice 2", padx=20, font=('Helvetica', 30))
choice2.grid(row=0, column=1)
choice3 = Label(choiceFrame, text="Choice 3", padx=20, font=('Helvetica', 30))
choice3.grid(row=0, column=2)

root.mainloop()