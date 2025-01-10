from threading import Thread
import tkinter as tk
from tkinter import messagebox
from gameState import gameState
from bot import ai
from multiprocessing import freeze_support

class game :
  def __init__(self, botOn, window): 
    self.window = window
    self.window.title("Queens barcade")
    self.window.geometry("152x152")
    self.peice = (tk.PhotoImage(file="queen p1.png"),tk.PhotoImage(file="queen p2.png"))
    self.white = tk.PhotoImage(file="white.png")
    self.wall = tk.PhotoImage(file="wall.png")
    self.state = gameState((set(),(13,14,0,3),True))
    self.botOn = botOn
    self.space = []
    self.processing = False
    self.thread = None
    for i in range (16):
      self.space.append(tk.Button(self.window,image=self.white,height=32,width=32,bd=2,bg="black",relief='flat',highlightthickness=0,command=lambda num=i :self.click(num)))
      self.space[i].grid(row=i//4,column=i%4)
    for x in [13,14,0,3] :
      self.space[x].config(image = self.peice[int(((x+6)**-1)*10)])
    tk.mainloop()

  def click(self,loc):
    if self.processing :
      return False
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
      self.space[loc].config(image = self.wall)
    else:
      self.space[self.state.peiceSelected].config(image=self.white,bg="black")
      self.space[loc].config(image = self.peice[0 if self.state.p1Turn else 1])
    self.state = gameState(newState)

    end = self.state.endingBoard()
    if end == -1000000:
      messagebox.showinfo('Game end',"P1 win")
    elif end == 0:
      messagebox.showinfo('Game end',"Tie")
    elif end == 1000000:
      messagebox.showinfo('Game end', "P2 win")
    if end != None:
      for space in self.space:
        space.destroy()
      self.window.quit()
    if self.botOn and not self.state.p1Turn:
      self.processing = True
      self.thread = Thread(target=self.process).start()
    return False
  
  def process(self):
    move = ai(self.state)
    self.processing = False
    self.click(move)

if __name__ == "__main__":
  freeze_support()