import tkinter as tk
from tkinter import messagebox
import random
import subprocess
import simplejson



window = tk.Tk()
window.title("Queens barcade")
window.geometry("152x152")

botOn = True
with open('botOn.jason') as bot:
  botOn = simplejson.load(bot)


ai = {}
moves = []
defultProbMap = []
if botOn :
  with open('ai.jason') as aiData:
    ai = simplejson.load(aiData)
  for num in range(16) :
    defultProbMap.append([.1,.1])


peice = [tk.PhotoImage(file="queen p1.png"),tk.PhotoImage(file="queen p2.png")]
white = tk.PhotoImage(file="white.png")
wall = tk.PhotoImage(file="wall.png")
wallLocations = ""
peiceLoactions = "de03"
peiceSelected = -1
p1Turn = True
winCon = ''
again = "no"

def bot() :
  global ai
  global moves
  map = ("".join(sorted(peiceLoactions[:2])) + "".join(sorted(peiceLoactions[2:])) + "".join(sorted(wallLocations)))
  rand = random.randint(0,15)
  while random.randint(0,ai.get(map,defultProbMap)[rand][(peiceSelected+4)//4]*100//1) :
    rand = random.randint(0,15)
  moves.append([map,rand,(peiceSelected+4)//4])
  return rand

def inLoc(loc) :
  for i in range(4) :
      if hex(loc)[-1] == peiceLoactions[i] :
        return i
  return -1
def surounded(loc,isPlayer1) :
  if loc == "g" :
    return False
  loc = int(loc,base=16)
  surrounding = []
  if int(loc / 4) > 0:
    surrounding.append(loc - 4)
    if loc % 4 > 0:
      surrounding.append(loc - 5)
    if loc % 4 < 3:
      surrounding.append(loc - 3)
  if int(loc / 4) < 3:
    surrounding.append(loc + 4)
    if loc % 4 > 0:
      surrounding.append(loc + 3)
    if loc % 4 < 3:
      surrounding.append(loc + 5)
  if loc % 4 > 0:
    surrounding.append(loc - 1)
  if loc % 4 < 3:
    surrounding.append(loc + 1)
  for i in range(len(surrounding)) :
    if not(hex(surrounding[i])[-1] in wallLocations or (hex(surrounding[i])[-1] in peiceLoactions[:2] and isPlayer1) or (hex(surrounding[i])[-1] in peiceLoactions[2:] and not isPlayer1)): 
      return False
  return True

def inLine(loc) :
  if peiceSelected == -1 or int(peiceLoactions[peiceSelected],base=16) == loc:
    return True
  toAdd = [-5,-4,-3,-1,1,3,4,5]
  for j in range(8) :
    i = int(peiceLoactions[peiceSelected],base=16) + toAdd[j]
    cont = True
    while (i >= 0 and i < 16) and cont:
      if hex(i)[-1] in wallLocations or ((p1Turn and hex(i)[-1] in peiceLoactions[:2]) or (not p1Turn and hex(i)[-1] in peiceLoactions[2:])) or (hex(i)[-1] in peiceLoactions and i !=loc) or (((i-toAdd[j])%4==0 and (i)%4==3) or ((i-toAdd[j])%4==3 and (i)%4==0)) :
        cont = False
      elif i == loc :
        return True
      i+=toAdd[j]
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

space = []
for i in range (16):
  space.append( tk.Button(window,image=white,height=32,width=32,bd=2,bg="black",relief='flat',highlightthickness=0,command=lambda num=i :click(num)))
  space[i].grid(row=i//4,column=i%4)
for x in [13,14,0,3] :
  space[x].config(image = peice[int(((x+6)**-1)*10)])
tk.mainloop()

winCon = False if winCon == 'tie' else (.5 if winCon == "P2 win" else 2)
if botOn and winCon :
  for game in moves :
    probMap = ai.get(game[0],defultProbMap.copy())
    probMap[game[1]][game[2]]*=winCon
    ai.setdefault(game[0],probMap)
  with open('ai.jason','w') as aiData:
    simplejson.dump(ai,aiData)
if again == 'yes' :
  subprocess.run(["python", "game.py"])
else :
  subprocess.run(["python", "main.py"])