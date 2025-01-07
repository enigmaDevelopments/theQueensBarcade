from gameState import gameState


def ai(state) :
  alpha = -200
  best = -200
  bestMove = None
  for node in state.vaildMoves():
    value = minMax(gameState(state.move(node)),1,alpha,2)
    if value > best:
      best = value
      bestMove = node
      if best > alpha:
        alpha = best
  return bestMove

def minMax(state : gameState, depth, alpha, beta):
  end = state.endingBoard()
  if end != None:
    return end
  if depth == 5:
    p1 = {i[1] for i in state.vaildPeiceMoves(True)}
    p2 = {i[1] for i in state.vaildPeiceMoves(False)}
    p12 = p1 - p2
    p22 = p2 - p1
    return len(p22)-len(p12)
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