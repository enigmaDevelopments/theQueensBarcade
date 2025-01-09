
import tkinter as tk
import subprocess
from game import game





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

  game(botOn, window)

  elements()
def howToPlay() :
  subprocess.run(["python", "howToPlay.py"])  

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
  window = tk.Tk()
  elements()
  tk.mainloop()
