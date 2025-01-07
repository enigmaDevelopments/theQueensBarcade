from gameState import gameState


def ai(state) :
  alpha = -2
  best = -2
  bestMove = None
  for node in state.vaildMoves():
    value = minMax(gameState(state.move(node)),1,alpha,2)
    if value > best:
      best = value
      bestMove = node
      if best > alpha:
        alpha = best
  return bestMove

def minMax(state, depth, alpha, beta):
  end = state.endingBoard()
  if end != None:
    return end
  if state.p1Turn:
    best = 2
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
    best = -2
    for node in state.vaildMoves():
      value = minMax(gameState(state.move(node)),depth+1,alpha,beta)
      if value > best:
        best = value
        if best > alpha:
          alpha = best
          if beta <= alpha:
            break
    return best