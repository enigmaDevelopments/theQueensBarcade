import cupy as cp

edges = cp.array((
    ((True,True,True,False),
     (True,True,True,False),
     (True,True,True,False),
     (False,False,False,False)),

    ((True,True,True,True),
     (True,True,True,True),
     (True,True,True,True),
     (False,False,False,False)),

    ((False,True,True,True),
     (False,True,True,True),
     (False,True,True,True),
     (False,False,False,False)),

    ((True,True,True,False),
     (True,True,True,False),
     (True,True,True,False),
     (True,True,True,False)),
     
    ((False,True,True,True),
     (False,True,True,True),
     (False,True,True,True),
     (False,True,True,True)),

    ((False,False,False,False),
     (True,True,True,False),
     (True,True,True,False),
     (True,True,True,False)),

    ((False,False,False,False),
     (True,True,True,True),
     (True,True,True,True),
     (True,True,True,True)),

    ((False,False,False,False),
     (False,True,True,True),
     (False,True,True,True),
     (False,True,True,True)),
))

surrounding = cp.array((
    (((-.5,1,0,0),
     (1,1,0,0),
     (0,0,0,0),
     (0,0,0,0)),

    ((1,-.5,1,0),
     (1,1,1,0),
     (0,0,0,0),
     (0,0,0,0)),

    ((0,1,-.5,1),
     (0,1,1,1),
     (0,0,0,0),
     (0,0,0,0)),

    ((0,0,1,-.5),
     (0,0,1,1),
     (0,0,0,0),
     (0,0,0,0))),


    (((1,1,0,0),
     (-.5,1,0,0),
     (1,1,0,0),
     (0,0,0,0)),

    ((1,1,1,0),
     (1,-.5,1,0),
     (1,1,1,0),
     (0,0,0,0)),

    ((0,1,1,1),
     (0,1,-.5,1),
     (0,1,1,1),
     (0,0,0,0)),

    ((0,0,1,1),
     (0,0,1,-.5),
     (0,0,1,1),
     (0,0,0,0))),


    (((0,0,0,0),
     (1,1,0,0),
     (-.5,1,0,0),
     (1,1,0,0)),
      
    ((0,0,0,0),
     (1,1,1,0),
     (1,-.5,1,0),
     (1,1,1,0)),

    ((0,0,0,0),
     (0,1,1,1),
     (0,1,-.5,1),
     (0,1,1,1)),

    ((0,0,0,0),
     (0,0,1,1),
     (0,0,1,-.5),
     (0,0,1,1))),


    (((0,0,0,0),
     (0,0,0,0),
     (1,1,0,0),
     (-.5,1,0,0)),

    ((0,0,0,0),
     (0,0,0,0),
     (1,1,1,0),
     (1,-.5,1,0)),

    ((0,0,0,0),
     (0,0,0,0),
     (0,1,1,1),
     (0,1,-.5,1)),

    ((0,0,0,0),
     (0,0,0,0),
     (0,0,1,1),
     (0,0,1,-.5)))
))

directions = cp.array((-5,-4,-3,-1,1,3,4,5))

def score(walls: cp.ndarray, pieces: cp.ndarray):
    return 0

def getMoves(walls: cp.ndarray, p1: cp.ndarray,p2: cp.ndarray,p3: cp.ndarray,p4: cp.ndarray, p1Turn: bool):
    global edges
    global directions

    if p1Turn:
        player = (p1 * 2) + (p2 * 4)
        wall = cp.array((walls & ~(p3|p4), walls & ~(p1|p2|p3|p4)))
    else:
        player = (p3 * 2) + (p4 * 4)
        wall = cp.array((walls & ~(p1|p2), walls & ~(p1|p2|p3|p4)))

    moves = cp.zeros(cp.shape(walls),cp.int8)

    for i in cp.arange(8):
        pos = player.copy()
        block = wall & edges[i]

        for _ in cp.arange(3):
            pos = cp.roll(pos,directions[i])
            moves += pos * block[0]
            pos *= block[1]
    return cp.array((wall[1],moves & 2, moves & 4),cp.bool_)

walls = cp.array(((False,True,True,True),(True,True,True,True),(True,False,True,True),(True,True,True,True)))
p1 = cp.array(((False,False,False,False),(False,False,False,False),(False,False,False,False),(True,False,False,False)))
p2 = cp.array(((False,False,False,False),(False,False,False,False),(False,False,False,False),(False,False,False,True)))
p3 = cp.array(((False,True,False,False),(False,False,False,False),(False,False,False,False),(False,False,False,False)))
p4 = cp.array(((False,False,True,False),(False,False,False,False),(False,False,False,False),(False,False,False,False)))
pieces = cp.array((((0,1),(0,2)),((3,0),(3,3))))

walls = cp.array((walls,walls))
p1 = cp.array((p1,p1))
p2 = cp.array((p2,p2))
p3 = cp.array((p3,p3))
p4 = cp.array((p4,p4))
pieces = cp.array((pieces,pieces))

moves = getMoves(walls,p1,p2,p3,p4, True)
print (moves)