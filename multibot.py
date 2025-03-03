from concurrent import futures
from gameState import gameState
from random import choice
from multiprocessing import freeze_support
from bot import minMax
  
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