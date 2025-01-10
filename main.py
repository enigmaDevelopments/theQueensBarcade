import tkinter as tk
from game import game
from multiprocessing import freeze_support





def startGame(botOn) :
  global window
  global gameLabel
  global sPlayer
  global mPlayer
  global howTo
  
  gameLabel.destroy()
  sPlayer.destroy()
  mPlayer.destroy()
  howTo.destroy()

  again = "yes"
  while (again == "yes"):
    game(botOn, window)
    again = tk.messagebox.askquestion('Game end', 'Play again?')

  elements()
def howToPlay() :
  window2 = tk.Tk()
  window2.title("How to play")
  window2.geometry("400x250")

  title = tk.Label(window2,text = "How to play",font=("Impact", 18))
  explenation = tk.Label(window2,text = "Each player has 2 queens, each queen can move up, down, left, right or dignal in a line until it hits an object. On you turn your you may also choose to place down a wall. A Queen can not go through a wall or anouther queen. If a queen lands on an opponents queen then their queen is is captured. If you capture both of your opponents queens or if an opponent can not move there queens you win. If neither player can move a queen the game ends in a tie.",font=("Comic Sans MS", 12), pady = 10,wraplength=400)
  title.pack()
  explenation.pack()
  tk.mainloop()

def elements():
  global window
  global gameLabel
  global sPlayer
  global mPlayer
  global howTo
  
  window.title("start screen")
  window.geometry("200x170")

  gameLabel = tk.Label(window,text = "The Queens\nBarcade",font=("Impact", 24))

  sPlayer = tk.Button(window,text ="1 Player",height=1,width=5,bd=0,relief='flat',highlightthickness=0,command=lambda:startGame(True))
  mPlayer = tk.Button(window,text ="2 Player",height=1,width=5,bd=0,relief='flat',highlightthickness=0,command=lambda:startGame(False))
  howTo = tk.Button(window,text ="How to play",height=1,width=9,bd=0,relief='flat',highlightthickness=0, command = lambda:howToPlay())

  gameLabel.pack()
  sPlayer.pack()
  mPlayer.pack()
  howTo.pack()


if __name__ == "__main__":
  freeze_support()
  window = tk.Tk()
  elements()
  tk.mainloop()
