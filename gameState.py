class gameState:
    def __init__(self, info: tuple) :
        self.wallLocations = info[0]
        self.peiceLoactions = info[1]
        self.p1Turn = info[2]
        self.peiceSelected = -1

    def surounded(self,loc : int,isPlayer1 : bool) :
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
        moves = []
        peices = self.peiceLoactions[:2] if self.p1Turn else self.peiceLoactions[2:]
        toAdd = (-5,-4,-3,-1,1,3,4,5)
        for i in peices:
            if i == 16:
                continue  
            for j in toAdd:
                h = i + j
                cont = True
                cont2 = True
                while (h >= 0 and h < 16) and cont:
                    if h in self.wallLocations or (((h-j)%4==0 and h%4==3) or ((h-j)%4==3 and (h)%4==0)) or not cont2 :
                        cont = False
                    elif (self.p1Turn and h in self.peiceLoactions[2:]) or (not self.p1Turn and h in self.peiceLoactions[:2]) :
                        cont2 = False
                        moves.append((i,h))
                    elif h in self.peiceLoactions :
                        cont = False
                    else:
                        moves.append((i,h))
                    h+=j
        return tuple(moves) + tuple(set(range(16)) - self.wallLocations-set(self.peiceLoactions))
    
    def score(self):
        peices =[set(),set()]
        toAdd = (-5,-4,-3,-1,1,3,4,5)
        for i,locs in zip(self.peiceLoactions,peices):
            if i == 16:
                continue
            for j in toAdd:
                h = i+j
                if 0 < h < 16 and (i%4!=0 or h%4!=3) and (i%4!=3 or h%4!=0):
                    locs.add(h)
        p1 = peices[0] - (set(self.peiceLoactions[:2]) | self.wallLocations)
        p2 = peices[1] - (set(self.peiceLoactions[2:]) | self.wallLocations)
        p1Score = len(p1-p2) + self.p1Turn / 2
        p2Score = len(p2-p1) + (not self.p1Turn) / 2
        if max (p1Score,p2Score) < min(p1Score,p2Score) + len(p1 & p2):
            return 0
        return p2Score - p1Score 
        
    
    def endingBoard (self) :
        peicesGone = [0,0]
        for i in range (4) :
            if self.surounded(self.peiceLoactions[i],not i//2):
                peicesGone[i//2] += 1
        if peicesGone[0] == 2 and peicesGone[1] == 2 :
            return 0
        elif peicesGone[0] == 2 :
            return 1000000
        elif  peicesGone[1] == 2 :
            return -1000000
    
    def move(self,loc):
        vaild = self.vaildMoves()
        if self.peiceSelected != -1:
            loc = (self.peiceSelected,loc)
        if loc in vaild :
            if type(loc) != tuple :
                return (self.wallLocations | {loc}, tuple(self.peiceLoactions), not self.p1Turn)
            peices = list(self.peiceLoactions)
            if loc[1] in peices:
                peices[peices.index(loc[1])] = 16
            peices[peices.index(loc[0])] = loc[1]
            return (self.wallLocations, tuple(sorted(peices[:2]) + sorted(peices[2:])), not self.p1Turn)  
        if type(loc) == tuple :
            if loc[0] == loc[1]:
                self.peiceSelected = -1
                return 1
            return
        for i in vaild :
            if type(i) != tuple :
                continue
            if loc == i[0]:
                self.peiceSelected = i[0]
                return 0