import tkinter as tk
from tkinter import messagebox
from gameState import gameState
from bot import ai

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
    if type(loc) == tuple:
      return self.click(loc[0]) and self.click(loc[1])
    newState = self.state.move(loc)
    if newState == None :
      return True
    elif newState == 0:
      self.space[loc].config(bg="green")
      return True
    elif newState == 1:
      self.space[loc].config(bg="black")
      return True
    if (self.state.peiceLoactions == newState[1]):
      print(loc)
      self.space[loc].config(image = self.wall)
    else:
      self.space[self.state.peiceSelected].config(image=self.white,bg="black")
      self.space[loc].config(image = self.peice[0 if self.state.p1Turn else 1])
    self.state = gameState(newState)
    end = self.state.endingBoard()
    winCon = None
    if end == -100:
      winCon = "P1 win"
    elif end == 0:
      winCon = "Tie"
    elif end == 100:
      winCon = "P2 win"
    if end != None:
      messagebox.showinfo('Game end', winCon)
      self.again = messagebox.askquestion('Game end', 'Play again?')
      self.window.destroy()

    if self.botOn and not self.state.p1Turn:
      self.click(ai(self.state))
    return False
  
test = game(True)