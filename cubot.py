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
positions = cp.array((p,p))
player = cp.where(positions < 5 ,positions,0)
walls = cp.array(((cp.array((w,w)) * cp.where(((5 < positions) | (positions == 0)),1,0)), cp.array((w,w)) * cp.where(positions == 0,1,0)))
moves = cp.zeros_like(positions)

for i in cp.arange(len(directions)):
    pos = player.copy()
    block = walls * edges[i]

    for j in cp.arange(3):
        pos = cp.roll(pos,directions[i])
        moves += pos * block[0]
        pos *= block[1]
p1Moves = moves & 2
p2Moves = moves & 4

print(walls[1])
print(p1Moves)
print(p2Moves)