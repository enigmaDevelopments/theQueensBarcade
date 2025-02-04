import cupy as cp

edges = cp.array((
    ((1,1,1,0),(1,1,1,0),(1,1,1,0),(0,0,0,0)),
    ((1,1,1,1),(1,1,1,1),(1,1,1,1),(0,0,0,0)),
    ((0,1,1,1),(0,1,1,1),(0,1,1,1),(0,0,0,0)),
    ((1,1,1,0),(1,1,1,0),(1,1,1,0),(1,1,1,0)),
    ((0,1,1,1),(0,1,1,1),(0,1,1,1),(0,1,1,1)),
    ((0,0,0,0),(1,1,1,0),(1,1,1,0),(1,1,1,0)),
    ((0,0,0,0),(1,1,1,1),(1,1,1,1),(1,1,1,1)),
    ((0,0,0,0),(0,1,1,1),(0,1,1,1),(0,1,1,1)),
))

directions = cp.array((-5,-4,-3,-1,1,3,4,5))

p = cp.array(((0,8,16,0),(0,0,0,0),(0,0,0,0),(2,0,0,4)))
w = cp.array(((0,1,1,1),(1,1,1,1),(1,0,1,1),(1,1,1,1)))

def getMoves(wall: cp.ndarray, positions: cp.ndarray):
    global edges
    global directions

    player = cp.where(positions < 5 ,positions,0)
    walls = cp.array(((wall * cp.where(((5 < positions) | (positions == 0)),1,0)), wall * cp.where(positions == 0,1,0)))
    moves = cp.zeros_like(positions)

    for i in cp.arange(len(directions)):
        pos = player.copy()
        block = walls * edges[i]

        for _ in cp.arange(3):
            pos = cp.roll(pos,directions[i])
            moves += pos * block[0]
            pos *= block[1]
    return cp.array((walls[1],moves & 2, moves & 4))

w = cp.array(((0,1,1,1),(1,1,1,1),(1,0,1,1),(1,1,1,1)))
p = cp.array(((0,8,16,0),(0,0,0,0),(0,0,0,0),(2,0,0,4)))

moves = getMoves(cp.array((w,w)),cp.array((p,p)))
print (moves)