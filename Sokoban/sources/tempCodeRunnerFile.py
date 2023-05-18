def breadthFirstSearch(gameState):
    """Implement breadthFirstSearch approach"""
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)

    startState = (beginPlayer, beginBox) # e.g. ((2, 2), ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5)))
    frontier = collections.deque([[startState]]) # store states
    actions = collections.deque([[0]]) # store actions
    exploredSet = set()
    temp = []

    ### Implement breadthFirstSearch here

    while frontier: 
        node = frontier.popleft() 
        node_action = actions.popleft() 
        if isEndState(node[-1][-1]):
            temp += node_action[1:] 
            break
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1]) 
            for action in legalActions(node[-1][0], node[-1][1]): 
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action) 
                if isFailed(newPosBox): 
                    continue 
                frontier.append(node + [(newPosPlayer, newPosBox)]) 
                actions.append(node_action + [action[-1]]) 
    return temp