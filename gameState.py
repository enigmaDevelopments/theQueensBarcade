class gameState:
    def __init__(self, info):
        self.wallLocations = info[0]
        self.peiceLoactions = info[1]
        self.prevStates = info[2]
        self.p1Turn = info[3]
        self.peiceSelected = -1

    def surounded(self,loc,isPlayer1) :
        if loc == 16:
            return True
        surrounding = set()
        if loc // 4 > 0:
            surrounding.add(loc - 4)
            if loc % 4 > 0:
                surrounding.add(loc - 5)
            if loc % 4 < 3:
                surrounding.add(loc - 3)
        if loc // 4 < 3:
            surrounding.add(loc + 4)
            if loc % 4 > 0:
                surrounding.add(loc + 3)
            if loc % 4 < 3:
                surrounding.add(loc + 5)
        if loc % 4 > 0:
            surrounding.add(loc - 1)
        if loc % 4 < 3:
            surrounding.add(loc + 1)
        return  surrounding <= (self.wallLocations | set(self.peiceLoactions[:2] if isPlayer1 else self.peiceLoactions[2:]))

    def vaildMoves(self) :
        moves = list(set(range(16)) - self.wallLocations-set(self.peiceLoactions))
        peices = self.peiceLoactions[:2] if self.p1Turn else self.peiceLoactions[2:]
        toAdd = (-5,-4,-3,-1,1,3,4,5)
        for i in peices:
            if i == 16:
                continue  
            move = [i]
            for j in toAdd:
                h = i + j
                cont = True
                cont2 = True
                while (h >= 0 and h < 16) and cont:
                    if h in self.wallLocations or (((h-j)%4==0 and h%4==3) or ((h-j)%4==3 and (h)%4==0)) or not cont2 :
                        cont = False
                    elif (self.p1Turn and h in self.peiceLoactions[2:]) or (not self.p1Turn and h in self.peiceLoactions[:2]) :
                        cont2 = False
                        move.append(h)
                    elif h in self.peiceLoactions :
                        cont = False
                    else:
                        move.append(h)
                    h+=j
            moves.append(tuple(move))
        return tuple(moves)
    
    def endingBoard (self) :
        peicesGone = [0,0]
        for i in range (4) :
            if self.surounded(self.peiceLoactions[i],not i//2):
                peicesGone[i//2] += 1
        print(peicesGone)
        if peicesGone[0] == 2 and peicesGone[1] == 2 :
            return 2
        elif peicesGone[0] == 2 :
            return 3
        elif  peicesGone[1] == 2 :
            return 1
        elif self.prevStates.count(self.peiceLoactions) == 2 :
            return 2
        return 0
    
    def move(self,loc):
        vaild = self.vaildMoves()
        for i in vaild :
            if type(i) == tuple :
                if self.peiceSelected == i[0] and loc[0] in i[1:] and loc[0] != self.peiceSelected:
                    return self.peiceMove(loc[0])
                elif self.peiceSelected == -1 and loc[0] == i[0] :
                    if len(loc) == 2 and loc[1] in i:
                        self.peiceSelected = loc[0]
                        return self.peiceMove(loc[1])
                    else:
                        self.peiceSelected = i[0]
                        return 0
        if loc[0] in vaild:
            return (self.wallLocations | {loc[0]}, tuple(self.peiceLoactions), (), not self.p1Turn)
        if self.peiceSelected == loc[0]:
            self.peiceSelected = -1
            return 1
    
    def peiceMove(self, loc):
        peices = list(self.peiceLoactions)
        if loc in peices:
            peices[peices.index(loc)]  = 16
        peices[peices.index(self.peiceSelected)]  = loc
        return (self.wallLocations, tuple(peices), self.prevStates + (self.peiceLoactions,), not self.p1Turn)