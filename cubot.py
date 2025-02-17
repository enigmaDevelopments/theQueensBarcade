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

empty = cp.array((
    False,False,False,False,
     False,False,False,False,
     False,False,False,False,
     False,False,False,False
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

def getScore(gameStates: cp.ndarray, p1Turn: bool):
    global surrounding
    shape = gameStates.shape

    i = cp.arange(4)
    idx = cp.argwhere(gameStates[i]).T
    merged = cp.full((4,shape[1]),cp.int8(16))
    merged[idx[0],idx[1]] = idx[2]
    nears = (surrounding[merged])

    player1 = (nears[0]|nears[1]) & ~(gameStates[0]|gameStates[1]) & gameStates[4]
    player2 = (nears[2]|nears[3]) & ~(gameStates[2]|gameStates[3]) & gameStates[4]

    p1Sum = cp.sum(player1&~player2,1,cp.float16)
    p2Sum = cp.sum(player2&~player1,1,cp.float16)
    p1NotZero = p1Sum.astype(bool)
    p2NotZero = p2Sum.astype(bool)
    p1Sum += cp.float16(p1Turn * .5)
    p2Sum += cp.float16((not p1Turn) *.5)
    bSum = cp.sum(player1&player2,1,cp.float16)
    total = p2Sum - p1Sum

    return cp.where(p1NotZero, cp.where(p2NotZero, cp.where(cp.fabs(total)<bSum,0,total), -100), cp.where(p2NotZero,100,0))

    



def getMoves(gameStates: cp.ndarray, p1Turn: bool):
    global edges
    global directions

    player = cp.reshape(cp.tile(gameStates[0 if p1Turn else 2] + (gameStates[1 if p1Turn else 3] * cp.int8(2)), (8, 1, 1)),(8,-1))
    wall = cp.array((gameStates[4] & ~(gameStates[2 if p1Turn else 0]|gameStates[3 if p1Turn else 1]), gameStates[4] & ~(gameStates[0]|gameStates[1]|gameStates[2]|gameStates[3])))
    shape = player.shape
    moves = cp.zeros(shape[1],cp.int8)

    block = cp.reshape(wall[:,None, :, :] & edges[None,:,None, :],(2,8,-1))
    i = cp.arange(8)[:, None]
    j = (cp.tile(cp.arange(shape[1]),(8, 1)) - directions[:, None]) % shape[1]

    for _ in range(3):
        player = player[i,j]
        moves += cp.sum(player * block[0],0)
        player *= block[1]
    return cp.array((cp.reshape(moves&1,(-1,16)),cp.reshape(moves&2,(-1,16)),wall[1]),cp.bool_)


def makeMoves(gameStates: cp.ndarray,moves: cp.ndarray, p1Turn: bool):
    global empty
    size = gameStates.shape[1]
    
    peiceLoc = cp.argwhere(moves[:2])
    peiceLoc = peiceLoc[cp.argsort(peiceLoc.T[1])].T
    inversePeiceLoc = cp.setdiff1d(cp.arange(size),peiceLoc[1])
    moves[2][inversePeiceLoc] = empty
    wallLoc = cp.argwhere(moves[2])
    wallLoc = wallLoc[cp.argsort(wallLoc.T[0])].T
    tLoc = cp.sort(cp.concatenate((peiceLoc[1],wallLoc[0],inversePeiceLoc)))
    #print(tLoc)
    output = cp.transpose(gameStates,(1,0,2))[tLoc]

    wallAmounts =  cp.bincount(wallLoc[0],minlength=size)
    peiceAmounts = cp.bincount(peiceLoc[1],minlength=size)
    totalAmounts = wallAmounts + peiceAmounts
    mask = totalAmounts == 0
    cp.putmask(totalAmounts,mask,1)

    idx = cp.cumsum(totalAmounts)
    
    fullIdx = cp.arange(idx[-1])
    wallIdx = idx - wallAmounts
    
    iStart = cp.roll(cp.cumsum(wallAmounts),1)
    iSize = iStart[0].item()
    iStart[0] = 0

    flatIdx = cp.arange(iSize)
    offsets = flatIdx - cp.take(iStart, wallLoc[0])
    mappedIdx = cp.take(wallIdx, wallLoc[0]) + offsets

    #print(mappedIdx.shape)

    i = fullIdx[mappedIdx]
    output[i,4,wallLoc[1]] = False

    noneIdx = idx[cp.argwhere(mask)] - 1
    i = cp.setdiff1d(cp.setdiff1d(fullIdx,i,True),noneIdx,True)

    if not p1Turn:
        peiceLoc[0] += 2
    moveMask = ~output[i,peiceLoc[0]]
    output[i,2 if p1Turn else 1] &= moveMask
    output[i,3 if p1Turn else 1] &= moveMask
    output[i,peiceLoc[0]] &= False
    output[i,peiceLoc[0],peiceLoc[2]] = True

    offsets = cp.zeros_like(idx)
    offsets[1:] = idx[:-1]  # Starting indices for each group
    groupIds = cp.searchsorted(offsets, fullIdx, side='right') - 1
    idxMap = fullIdx - offsets[groupIds]
    
    return (cp.array((tLoc,idxMap)),cp.transpose(output,(1,0,2)))

def minMax(gameStates :cp.ndarray):
    p1Turn = False
    idxs = []
    for _ in range(6):
        idx,gameStates = makeMoves(gameStates,getMoves(gameStates,p1Turn),p1Turn)
        idxs.insert(0,idx)
        p1Turn = not p1Turn
    scores = getScore(gameStates,True)
    for i, j  in idxs:
        r = cp.max(i).item()
        c = cp.max(j).item()
        k = cp.arange(i.size)
        oldScores = +scores
        if p1Turn:
            partitioned = cp.full((r+1,c+1),200)
            partitioned[i, j] = scores[k]
            scores = cp.min(partitioned,1)
        else:
            partitioned = cp.full((r+1,c+1),-200)
            partitioned[i, j] = scores[k]
            scores = cp.max(partitioned,1) 
        p1Turn = not p1Turn 
    return cp.random.choice(cp.ravel(cp.argwhere(scores.item() == oldScores)),1).item()
        

    
    
    



walls = cp.array((False,True,True,True, True,True,True,True, True,False,True,True, True,True,True,True))
p1 = cp.array((False,False,False,False, False,False,False,False, False,False,False,False, True,False,False,False))
p2 = cp.array((False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,True))
p3 = cp.array((False,True,False,False, False,False,False,False, False,False,False,False, False,False,False,False))
p4 = cp.array((False,False,True,False, False,False,False,False, False,False,False,False, False,False,False,False))

# walls = cp.array((walls,walls,walls,walls))
# p1 = cp.array((p1,empty,empty,p1))
# p2 = cp.array((p2,empty,empty,p2))
# p3 = cp.array((p3,p3,p3,p3))
# p4 = cp.array((p4,p4,p4,p4))

gameStates = cp.array((p1,p2,p3,p4,walls))[:, None, :]

moves = getMoves(gameStates, True)
#moves = cp.reshape(moves,(3,-1,4,4))
#print (moves)

score = getScore(gameStates, True)
#print(score)

idx, state = makeMoves(gameStates, moves, True)

print(minMax(gameStates))