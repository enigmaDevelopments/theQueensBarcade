from concurrent import futures
from gameState import gameState
from random import choice
from multiprocessing import freeze_support


def minMax(state : gameState, depth, alpha, beta):
  end = state.endingBoard()
  if end == 0:
    return 1/(depth+2)
  if end != None:
    return end + ((depth*1000) + state.score() if end < 0 else -depth)
  if depth == 7:
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
  
def thread(info):
  data = (minMax(info[0],1,-2000000,2000000), info[1])
  return data
  
def ai(state):
  best = -2000000
  bestMove = None
  games = ((gameState(state.move(move)),move) for move in state.vaildMoves())
  with futures.ProcessPoolExecutor() as executer:
    values = [executer.submit(thread, node) for node in games]
    for future in futures.as_completed(values, timeout=None):
      value = future.result()
      if value[0] > best:
        best = value[0]
        bestMove = [value[1]]
      elif value[0] == best:
        bestMove.append(value[1])
  return choice(bestMove) 

if __name__ == "__main__":
  freeze_support()