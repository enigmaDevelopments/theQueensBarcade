from functools import lru_cache
from concurrent import futures
from gameState import gameState


@lru_cache
def minMax(state : gameState, depth, alpha, beta):
  end = state.endingBoard()
  if end != None:
    return end
  if depth == 8:
    return state.score()
  if state.p1Turn:
    best = 200
    for node in state.vaildMoves():
      value = minMax(gameState(state.move(node)),depth+1,alpha,beta)
      if value < best:
        best = value
        if best < beta:
          beta = best
          if beta <= alpha:
            break
    return best
  else:
    best = -200
    for node in state.vaildMoves():
      value = minMax(gameState(state.move(node)),depth+1,alpha,beta)
      if value > best:
        best = value
        if best > alpha:
          alpha = best
          if beta <= alpha:
            break
    return best
  
def thread(info):
  return (minMax(info[0],1,-200,200), info[1])
  
def ai(state):
  best = -200
  bestMove = None
  games = ((gameState(state.move(move)),move) for move in state.vaildMoves())
  with futures.ProcessPoolExecutor() as executer:
    values = [executer.submit(thread, node) for node in games]
    for future in futures.as_completed(values):
      value = future.result()
      if value[0] > best:
        best = value[0]
        bestMove = value[1]
  return bestMove 

if __name__ == '__main__':

  print(ai(gameState((set(),(13,14,0,3),False))))
