import tkinter as tk

window = tk.Tk()
window.title("How to play")
window.geometry("400x250")

title = tk.Label(window,text = "How to play",font=("Impact", 18))
explenation = tk.Label(window,text = "Each player has 2 queens, each queen can move up, down, left, right or dignal in a line until it hits an object. On you turn your you may also choose to place down a wall. A Queen can not go through a wall or anouther queen. If a queen lands on an opponents queen then their queen is is captured. If you capture both of your opponents queens or if an opponent can not move there queens you win. If neither player can move a queen the game ends in a tie.",font=("Comic Sans MS", 12), pady = 10,wraplength=400)
title.pack()
explenation.pack()

tk.mainloop()