import cupy as cp

edges = cp.array((
    ((1,1,1,0),
     (1,1,1,0),
     (1,1,1,0),
     (0,0,0,0)),

    ((1,1,1,1),
     (1,1,1,1),
     (1,1,1,1),
     (0,0,0,0)),

    ((0,1,1,1),
     (0,1,1,1),
     (0,1,1,1),
     (0,0,0,0)),

    ((1,1,1,0),
     (1,1,1,0),
     (1,1,1,0),
     (1,1,1,0)),
     
    ((0,1,1,1),
     (0,1,1,1),
     (0,1,1,1),
     (0,1,1,1)),

    ((0,0,0,0),
     (1,1,1,0),
     (1,1,1,0),
     (1,1,1,0)),

    ((0,0,0,0),
     (1,1,1,1),
     (1,1,1,1),
     (1,1,1,1)),

    ((0,0,0,0),
     (0,1,1,1),
     (0,1,1,1),
     (0,1,1,1)),
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
     (0,1,-.5,1))

    ((0,0,0,0),
     (0,0,0,0),
     (0,0,1,1),
     (0,0,1,-.5)))
))

directions = cp.array((-5,-4,-3,-1,1,3,4,5))

def score(walls: cp.ndarray, pieces: cp.ndarray):
    return 0

def getMoves(walls: cp.ndarray, positions: cp.ndarray, p1Turn: bool):
    global edges
    global directions

    if p1Turn:
        player = cp.where(positions < 5 ,positions,0)
        wall = cp.array(((walls * cp.where(((5 < positions) | (positions == 0)),1,0)), walls * cp.where(positions == 0,1,0)))
    else:
        player = cp.where(((5 < positions) | (positions == 0)) ,positions,0)
        wall = cp.array(((walls * cp.where(positions < 5,1,0)), walls * cp.where(positions == 0,1,0)))
    
    moves = cp.zeros_like(walls)

    for i in cp.arange(len(directions)):
        pos = player.copy()
        block = wall * edges[i]

        for _ in cp.arange(3):
            pos = cp.roll(pos,directions[i])
            moves += pos * block[0]
            pos *= block[1]

    if p1Turn:
        return cp.array((wall[1],moves & 2, moves & 4))
    else:
        return cp.array((wall[1],moves & 8, moves & 16))

walls = cp.array(((0,1,1,1),(1,1,1,1),(1,0,1,1),(1,1,1,1)))
positions = cp.array(((0,8,16,0),(0,0,0,0),(0,0,0,0),(2,0,0,4)))
pieces = cp.array((((0,1),(0,2))((3,0),(3,3))))

walls = cp.array((walls,walls))
positions = cp.array((positions,positions))
pieces = cp.array((pieces,pieces))

moves = getMoves(walls,positions, True)
print (moves)