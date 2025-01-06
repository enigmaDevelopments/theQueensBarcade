import tkinter as tk
from tkinter import messagebox
import subprocess
import simplejson
from gameState import gameState

class game :
  def __init__(self, botOn): 
    self.window = tk.Tk()
    self.window.title("Queens barcade")
    self.window.geometry("152x152")
    self.peice = (tk.PhotoImage(file="queen p1.png"),tk.PhotoImage(file="queen p2.png"))
    self.white = tk.PhotoImage(file="white.png")
    self.wall = tk.PhotoImage(file="wall.png")
    self.state = gameState((set(),(13,14,0,3),(),True))
    self.botOn = botOn
    self.space = []
    self.again = None
    for i in range (16):
      self.space.append(tk.Button(self.window,image=self.white,height=32,width=32,bd=2,bg="black",relief='flat',highlightthickness=0,command=lambda num=i :self.click(num)))
      self.space[i].grid(row=i//4,column=i%4)
    for x in [13,14,0,3] :
      self.space[x].config(image = self.peice[int(((x+6)**-1)*10)])
    tk.mainloop()
    if self.again == "yes":
      game(botOn)

  def click(self,loc):
    newState = self.state.move((loc,))
    if newState == None :
      return True
    elif newState == 0:
      self.space[loc].config(bg="green")
      return True
    elif newState == 1:
      self.space[loc].config(bg="black")
      return True
    if (self.state.peiceLoactions == newState[1]):
      self.space[loc].config(image = self.wall)
    else:
      self.space[self.state.peiceSelected].config(image=self.white,bg="black")
      self.space[loc].config(image = self.peice[0 if self.state.p1Turn else 1])
    self.state = gameState(newState)
    end = self.state.endingBoard()
    winCon = None
    if end == 1:
      winCon = "P1 win"
    elif end == 2:
      winCon = "Tie"
    elif end == 3:
      winCon = "P2 win"
    if end != 0:
      messagebox.showinfo('Game end', winCon)
      self.again = messagebox.askquestion('Game end', 'Play again?')
      self.window.destroy()
    return False
    

      

      
    
    


def click(loc) :
  global peiceSelected
  global peiceLoactions
  global p1Turn
  global wallLocations
  global winCon
  global ai
  global moves
  global again
  isInLoc = inLoc(loc)
  if not inLine(loc) :
    return True
  elif peiceSelected != -1  :
    space[ int(peiceLoactions[peiceSelected],base=16)].config(bg="black")
    if int(peiceLoactions[peiceSelected],base=16) == loc :
      peiceSelected = -1
      return True
    if ((p1Turn and hex(loc)[-1] in peiceLoactions[:2]) or (not p1Turn and hex(loc)[-1] in peiceLoactions[2:])):
      return True
    if isInLoc != -1 :
      peiceLoactions = peiceLoactions[:isInLoc] + "g" + peiceLoactions[isInLoc+1:]
    space[loc].config(image = peice[int(peiceSelected/2)])
    space[ int(peiceLoactions[peiceSelected],base=16)].config(image = white)
    peiceLoactions = peiceLoactions[:peiceSelected] + hex(loc)[-1] + peiceLoactions[peiceSelected+1:]
    peiceSelected = -1
  else:
    if isInLoc != -1 :
      if (isInLoc < 2 and p1Turn) or (isInLoc >= 2 and not p1Turn) :
        peiceSelected = isInLoc
        space[loc].config(bg="green")
        if not p1Turn and botOn :
          moves.append(moves[-1])
      return True
    if hex(loc)[-1] in wallLocations :
      return True
    space[loc].config(image = wall)
    wallLocations += hex(loc)[-1]
    for i in range (4) :
      if surounded(peiceLoactions[i],not i//2):
        wallLocations += peiceLoactions[i]
        peiceLoactions = peiceLoactions[:i] + "g" + peiceLoactions[i+1:]
  p1Lose = peiceLoactions[0] == "g" and peiceLoactions[1] == "g"
  p2Lose = peiceLoactions[2] == "g" and peiceLoactions[3] == "g"
  if p1Lose and p2Lose :
    winCon = "Tie"
  elif p1Lose :
    winCon = "P2 win"
  elif  p2Lose:
    winCon = "P1 win"
  if winCon :
    messagebox.showinfo('Game end', winCon)
    again = messagebox.askquestion('Game end', 'Play again?')
    window.destroy()
    return False
  p1Turn = not p1Turn
  while not p1Turn and botOn and click(bot()) : 
    moves.pop()
  return False


test = game(False)