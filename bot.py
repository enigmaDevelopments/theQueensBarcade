from gameState import gameState
from random import choice
from multiprocessing import freeze_support


def minMax(state : gameState, depth, alpha, beta):
  end = state.endingBoard()
  if end == 0:
    return 1/(depth+2)
  if end != None:
    return end + ((depth*1000) + state.score() if end < 0 else -depth)
  if depth == 5:
    return state.score()
  if state.p1Turn:
    best = 2000000
    for node in state.vaildMoves():
      nextState = gameState(state.move(node))
      value = minMax(nextState,depth+1,alpha,beta)
      if value < best:
        best = value
        if best < beta:
          beta = best
          if beta <= alpha:
            break
    return best
  else:
    best = -2000000
    for node in state.vaildMoves():
      nextState = gameState(state.move(node))
      value = minMax(nextState,depth+1,alpha,beta)
      if value > best:
        best = value
        if best > alpha:
          alpha = best
          if beta <= alpha:
            break
    return best
  
def ai(state):
  best = -2000000
  bestMove = None
  for move in state.vaildMoves():
    value = minMax(gameState(state.move(move)),1,best,2000000)
    if value > best:
      best = value
      bestMove = [move]
    elif value == best:
      bestMove.append(move)

  return choice(bestMove) 

if __name__ == "__main__":
  freeze_support()