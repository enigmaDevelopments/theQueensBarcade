#  ***Please open game.py to see the actual code for the game***





import tkinter as tk
import subprocess
import simplejson



window = tk.Tk()
window.title("start screen")
window.geometry("200x170")

def startGame(botOn) :
  window.destroy()
  with open('botOn.jason','w') as bot: 
    simplejson.dump(botOn,bot)
  subprocess.run(["python", "game.py"])
def howToPlay() :
  subprocess.run(["python", "howToPlay.py"])  

gameLabel = tk.Label(window,text = "The Queens\nBarcade",font=("Impact", 24))

sPlayer = tk.Button(window,text ="1 Player",height=1,width=5,bd=0,relief='flat',highlightthickness=0,command=lambda:startGame(True))
mPlayer = tk.Button(window,text ="2 Player",height=1,width=5,bd=0,relief='flat',highlightthickness=0,command=lambda:startGame(False))
howTo = tk.Button(window,text ="How to play",height=1,width=9,bd=0,relief='flat',highlightthickness=0, command = lambda:howToPlay())

gameLabel.pack()
sPlayer.pack()
mPlayer.pack()
howTo.pack()

tk.mainloop()
