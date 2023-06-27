# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        foodsPos = newFood.asList()
        foodsPos = sorted(foodsPos, key = lambda pos: manhattanDistance(newPos, pos))
        closestFoodDist = 0
        if len(foodsPos) > 0:
          closestFoodDist = manhattanDistance(foodsPos[0], newPos)

        foodCount = successorGameState.getNumFood()
        foodFeature = - closestFoodDist - 15*foodCount

        activeGhostsPos = []
        for ghost in newGhostStates:
          if ghost.scaredTimer == 0:
            activeGhostsPos.append(ghost.getPosition())
        activeGhostsPos = sorted(activeGhostsPos, key = lambda pos: manhattanDistance(pos, newPos))
        closestActiveGhostDist = 0
        if len(activeGhostsPos) > 0:
          closestActiveGhostDist = manhattanDistance(activeGhostsPos[0], newPos)
        return closestActiveGhostDist + foodFeature

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        maxValue = float("-inf")
        maxAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextValue = self.getValue(nextState, 0, 1)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
        return maxAction

    def getValue(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(gameState,currentDepth)
        else:
            return self.minValue(gameState,currentDepth,agentIndex)

    def maxValue(self, gameState, currentDepth):
        maxValue = float("-inf")
        for action in gameState.getLegalActions(0):
            maxValue = max(maxValue, self.getValue(gameState.generateSuccessor(0, action), currentDepth, 1))
        return maxValue

    def minValue(self, gameState, currentDepth, agentIndex):
        minValue = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            if agentIndex == gameState.getNumAgents()-1:
                minValue = min(minValue, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0))
            else:
                minValue = min(minValue, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1))
        return minValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def maximizer(state, depth, a, b):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)    
          val = float("-inf")
          legalActions = state.getLegalActions()
          succState = [state.generateSuccessor(0,x) for x in legalActions]
          for each in succState:
            val = max(val, minimizer(each, depth, state.getNumAgents()-1, a, b))
            if val > b:
              return val
            a = max(a, val)
          return val


        def minimizer(state, depth, index, a, b):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)          
          val = float("inf")
          legalActions = state.getLegalActions(index)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          for each in succState:
            if index > 1:
              val = min(val, minimizer(each, depth, index-1, a, b))
            else:
              val = min(val, maximizer(each, depth-1, a, b))
            if val < a:
              return val
            b = min(b, val)
          return val

          
        legalActions = gameState.getLegalActions()
        move = Directions.STOP
        val = float("-inf")
        a = float("-inf")
        b = float("inf")
        for action in legalActions:
          tmp = minimizer(gameState.generateSuccessor(0,action), self.depth, gameState.getNumAgents()-1, a, b)
          if tmp>val:
            val = tmp
            move = action
          if val > b:
            return value
          a = max(a,val)
        return move



        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maximizer(state, depth=0):
            if state.isLose() or state.isWin() or depth == 0:
                #evaluate the leaves
                return self.evaluationFunction(state)
            val = float("-inf")
            legalActions = state.getLegalActions()
            succState = [state.generateSuccessor(0,x) for x in legalActions]
            for each in succState:
                val = max(val, minimizer(each, depth, state.getNumAgents()-1))
            return val


        def minimizer(state, depth=0, index=0):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)
          val = float("inf")
          legalActions = state.getLegalActions(index)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          temp = 0
          for each in succState:
            if index > 1:
              temp += minimizer(each, depth, index-1)
            else:
              temp += maximizer(each, depth-1)
          return float(temp)/len(succState)


        legalActions = gameState.getLegalActions()
        move = Directions.STOP
        val = float("-inf")
        for action in legalActions:
          tmp = minimizer(gameState.generateSuccessor(0,action), self.depth, gameState.getNumAgents()-1)
          if tmp > val:
            val = tmp
            move = action
        return move


def countRemainingFood(newFood):
    return sum([len(filter(lambda y: y, x)) for x in newFood])

def getGhostScore(newPos, newGhostStates):
    total, distances = 0, []
    for ghostState in newGhostStates:
        ghostCoordinate = ghostState.getPosition()
        distances.append(manhattanDistance(newPos, ghostCoordinate))
        # approachingGhosts = len(filter(lambda x: x < 5, distances))
        # if approachingGhosts:
        #     return -10*approachingGhosts
    return sum(distances)

def avgFoodDistance(newPos, newFood):
    distances = []
    for x, row in enumerate(newFood):
        for y, column in enumerate(newFood[x]):
            if newFood[x][y]:
                distances.append(manhattanDistance(newPos, (x,y)))
    avgDistance = sum(distances)/float(len(distances)) if (distances and sum(distances) != 0) else 1
    return avgDistance

def surroundingFood(newPos, newFood):
    count = 0
    for x in range(newPos[0]-2, newPos[0]+3):
        for y in range(newPos[1]-2, newPos[1]+3):
            if (0 <= x and x < len(list(newFood))) and (0 <= y and y < len(list(newFood[1]))) and newFood[x][y]:
                count += 1
    return count

def minGhostDistance(newPos, newGhostStates):
    distances = []
    for ghostState in newGhostStates:
        ghostCoordinate = ghostState.getPosition()
        distances.append(manhattanDistance(newPos, ghostCoordinate))
    if distances and min(distances) != 0:
        return min(distances)
    return 1


def betterEvaluationFunction(currentGameState):
  pos = currentGameState.getPacmanPosition()
  currentScore = scoreEvaluationFunction(currentGameState)

  if currentGameState.isLose(): 
    return -float("inf")
  elif currentGameState.isWin():
    return float("inf")

  # food distance
  foodlist = currentGameState.getFood().asList()
  manhattanDistanceToClosestFood = min(map(lambda x: util.manhattanDistance(pos, x), foodlist))
  distanceToClosestFood = manhattanDistanceToClosestFood

  # number of big dots
  # if we only count the number fo them, he'll only care about
  # them if he has the opportunity to eat one.
  numberOfCapsulesLeft = len(currentGameState.getCapsules())
  
  # number of foods left
  numberOfFoodsLeft = len(foodlist)
  
  # ghost distance

  # active ghosts are ghosts that aren't scared.
  scaredGhosts, activeGhosts = [], []
  for ghost in currentGameState.getGhostStates():
    if not ghost.scaredTimer:
      activeGhosts.append(ghost)
    else: 
      scaredGhosts.append(ghost)

  def getManhattanDistances(ghosts): 
    return map(lambda g: util.manhattanDistance(pos, g.getPosition()), ghosts)

  distanceToClosestActiveGhost = distanceToClosestScaredGhost = 0

  if activeGhosts:
    distanceToClosestActiveGhost = min(getManhattanDistances(activeGhosts))
  else: 
    distanceToClosestActiveGhost = float("inf")
  distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)
    
  if scaredGhosts:
    distanceToClosestScaredGhost = min(getManhattanDistances(scaredGhosts))
  else:
    distanceToClosestScaredGhost = 0 # I don't want it to count if there aren't any scared ghosts

  outputTable = [["dist to closest food", -1.5*distanceToClosestFood], 
                 ["dist to closest active ghost", 2*(1./distanceToClosestActiveGhost)],
                 ["dist to closest scared ghost", 2*distanceToClosestScaredGhost],
                 ["number of capsules left", -3.5*numberOfCapsulesLeft],
                 ["number of total foods left", 2*(1./numberOfFoodsLeft)]]

  score = 1    * currentScore + \
          -1.5 * distanceToClosestFood + \
          -2    * (1./distanceToClosestActiveGhost) + \
          -2    * distanceToClosestScaredGhost + \
          -20 * numberOfCapsulesLeft + \
          -4    * numberOfFoodsLeft
  return score

# Abbreviation
better = betterEvaluationFunction

