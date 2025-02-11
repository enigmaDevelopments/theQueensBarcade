import cupy as cp

edges = cp.array((
    (True,True,True,False,
     True,True,True,False,
     True,True,True,False,
     False,False,False,False),

    (True,True,True,True,
     True,True,True,True,
     True,True,True,True,
     False,False,False,False),

    (False,True,True,True,
     False,True,True,True,
     False,True,True,True,
     False,False,False,False),

    (True,True,True,False,
     True,True,True,False,
     True,True,True,False,
     True,True,True,False),
     
    (False,True,True,True,
     False,True,True,True,
     False,True,True,True,
     False,True,True,True),

    (False,False,False,False,
     True,True,True,False,
     True,True,True,False,
     True,True,True,False),

    (False,False,False,False,
     True,True,True,True,
     True,True,True,True,
     True,True,True,True),

    (False,False,False,False,
     False,True,True,True,
     False,True,True,True,
     False,True,True,True),
))

surrounding = cp.array((
    (False,True,False,False,
     True,True,False,False,
     False,False,False,False,
     False,False,False,False),

    (True,False,True,False,
     True,True,True,False,
     False,False,False,False,
     False,False,False,False),

    (False,True,False,True,
     False,True,True,True,
     False,False,False,False,
     False,False,False,False),

    (False,False,True,False,
     False,False,True,True,
     False,False,False,False,
     False,False,False,False),


    (True,True,False,False,
     False,True,False,False,
     True,True,False,False,
     False,False,False,False),

    (True,True,True,False,
     True,False,True,False,
     True,True,True,False,
     False,False,False,False),

    (False,True,True,True,
     False,True,False,True,
     False,True,True,True,
     False,False,False,False),

    (False,False,True,True,
     False,False,True,False,
     False,False,True,True,
     False,False,False,False),


    (False,False,False,False,
     True,True,False,False,
     False,True,False,False,
     True,True,False,False),
      
    (False,False,False,False,
     True,True,True,False,
     True,False,True,False,
     True,True,True,False),

    (False,False,False,False,
     False,True,True,True,
     False,True,False,True,
     False,True,True,True),

    (False,False,False,False,
     False,False,True,True,
     False,False,True,False,
     False,False,True,True),


    (False,False,False,False,
     False,False,False,False,
     True,True,False,False,
     False,True,False,False),

    (False,False,False,False,
     False,False,False,False,
     True,True,True,False,
     True,False,True,False),

    (False,False,False,False,
     False,False,False,False,
     False,True,True,True,
     False,True,False,True),

    (False,False,False,False,
     False,False,False,False,
     False,False,True,True,
     False,False,True,False),


     (False,False,False,False,
     False,False,False,False,
     False,False,False,False,
     False,False,False,False)

))

directions = cp.array((-5,-4,-3,-1,1,3,4,5))

def getScore(walls: cp.ndarray, p1: cp.ndarray,p2: cp.ndarray, p3: cp.ndarray, p4: cp.ndarray, p1Turn: bool):
    global surrounding
    shape = p1.shape
    nears = []
    for p in (p1,p2,p3,p4):
        idx = cp.argwhere(p).T
        merged = cp.full(shape[0],cp.int8(16))
        merged[idx[0]] = idx[1]
        nears.append(surrounding[merged])

    player1 = (nears[0]|nears[1]) & ~(p1|p2) & walls
    player2 = (nears[2]|nears[3]) & ~(p3|p4) & walls

    p1Sum = cp.sum(player1&~player2,1,cp.float16)
    p2Sum = cp.sum(player2&~player1,1,cp.float16)
    p1NotZero = p1Sum.astype(bool)
    p2NotZero = p2Sum.astype(bool)
    p1Sum += cp.float16(p1Turn * .5)
    p2Sum += cp.float16((not p1Turn) *.5)
    bSum = cp.sum(player1&player2,1,cp.float16)
    total = p2Sum - p1Sum

    return cp.where(p1NotZero, cp.where(p2NotZero, cp.where(cp.fabs(total)<bSum,0,total), -100), cp.where(p2NotZero,100,0))

    



def getMoves(walls: cp.ndarray, p1: cp.ndarray,p2: cp.ndarray,p3: cp.ndarray,p4: cp.ndarray, p1Turn: bool):
    global edges
    global directions

    if p1Turn:
        player = (p1 * cp.int8(2)) + (p2 * cp.int8(4))
        wall = cp.array((walls & ~(p3|p4), walls & ~(p1|p2|p3|p4)))
    else:
        player = (p3 * cp.int8(2)) + (p4 * cp.int8(4))
        wall = cp.array((walls & ~(p1|p2), walls & ~(p1|p2|p3|p4)))

    moves = cp.zeros(cp.shape(walls),cp.int8)

    for i in cp.arange(8):
        pos = player.copy()
        block = wall & edges[i]

        for _ in cp.arange(3):
            pos = cp.roll(pos,directions[i])
            moves += pos * block[0]
            pos *= block[1]
    return cp.array((wall[1],moves&2, moves&4),cp.bool_)

walls = cp.array((False,True,True,True, True,True,True,True, True,False,True,True, True,True,True,True))
p1 = cp.array((False,False,False,False, False,False,False,False, False,False,False,False, True,False,False,False))
p2 = cp.array((False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,True))
p3 = cp.array((False,True,False,False, False,False,False,False, False,False,False,False, False,False,False,False))
p4 = cp.array((False,False,True,False, False,False,False,False, False,False,False,False, False,False,False,False))

walls = cp.array((walls,walls,walls,walls))
p1 = cp.array((p1,p1,p1,p1))
p2 = cp.array((p2,p2,p2,p2))
p3 = cp.array((p3,p3,p3,p3))
p4 = cp.array((p4,p4,p4,p4))



moves = getMoves(walls,p1,p2,p3,p4, True)
moves = cp.reshape(moves,(-1,4,4))
print (moves)

score = getScore(walls,p1,p2,p3,p4, True)
print(score)