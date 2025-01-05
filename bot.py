import random
import subprocess
import simplejson



ai = {}
moveses = [[],[]]
defultProbMap = []
with open('ai.jason') as aiData:
  ai = simplejson.load(aiData)
for num in range(16) :
  defultProbMap.append([.1,.1])


wallLocations = ""
peiceLoactions = "de03"
peiceSelected = -1
p1Turn = True
winCon = ''

def bot(moves) :
  global ai
  map = (("".join(sorted(peiceLoactions[2:])) + "".join(sorted(peiceLoactions[:2])) ) if p1Turn else ("".join(sorted(peiceLoactions[:2])) + "".join(sorted(peiceLoactions[2:]))) + "".join(sorted(wallLocations)))
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

def click(loc,moves) :
  global peiceSelected
  global peiceLoactions
  global p1Turn
  global wallLocations
  global winCon
  global ai
  global moveses
  isInLoc = inLoc(loc)
  if not inLine(loc) :
    return True
  elif peiceSelected != -1  :
    if int(peiceLoactions[peiceSelected],base=16) == loc :
      peiceSelected = -1
      return True
    if ((p1Turn and hex(loc)[-1] in peiceLoactions[:2]) or (not p1Turn and hex(loc)[-1] in peiceLoactions[2:])):
      return True
    if isInLoc != -1 :
      peiceLoactions = peiceLoactions[:isInLoc] + "g" + peiceLoactions[isInLoc+1:]
    peiceLoactions = peiceLoactions[:peiceSelected] + hex(loc)[-1] + peiceLoactions[peiceSelected+1:]
    peiceSelected = -1
  else:
    if isInLoc != -1 :
      if (isInLoc < 2 and p1Turn) or (isInLoc >= 2 and not p1Turn) :
        peiceSelected = isInLoc
        moves.append(moves[-1])
      return True
    if hex(loc)[-1] in wallLocations :
      return True
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

    return False
  p1Turn = not p1Turn
  while not p1Turn and click(bot(moveses[1]),moveses[1]) : 
    moveses[1].pop()
  return True

while click(bot(moveses[0]),moveses[0]):
  moveses[0].pop()

winCon = False if winCon == 'tie' else (.5 if winCon == "P2 win" else 2)
count = -1
if winCon :
  for moves in moveses :
    for game in moves :
      probMap = ai.get(game[0],defultProbMap.copy())
      probMap[game[1]][game[2]]*=winCon**count
      ai.setdefault(game[0],probMap)
    count+=2
  with open('ai.jason','w') as aiData:
    simplejson.dump(ai,aiData)
print(winCon)
subprocess.run(["python", "bot.py"])