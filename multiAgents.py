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
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        totalScore = 0.0
        for i in range(len(newGhostStates)):
            if newScaredTimes[i] >= manhattanDistance(newGhostStates[i].getPosition(), newPos):
                totalScore += 200
        x, y = newPos
        foodValues = currentGameState.getFood()
        distToFood = 0
        if not newFood.asList():
            distToFood = 1
        else:
            distToFood = 1 / min([manhattanDistance(newPos, foodPos)
                                  for foodPos in newFood.asList()])
        return successorGameState.getScore() + distToFood


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def minAction(gameState, depth, agentIndex):
            if depth < 0 or gameState.isLose() or gameState.isWin():
                return (self.evaluationFunction(gameState), Directions.STOP)
            v = float("inf")
            worstAction = Directions.STOP
            func = maxAction
            nextAgent = 0
            if agentIndex < gameState.getNumAgents() - 1:
                func = minAction
                nextAgent = agentIndex + 1
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                resultV = func(successor, depth, nextAgent)[0]
                if v > resultV:
                    v = resultV
                    worstAction = action
            return (v, worstAction)

        def maxAction(gameState, depth, agentIndex):
            if depth <= 0 or gameState.isLose() or gameState.isWin():
                return (self.evaluationFunction(gameState), Directions.STOP)
            v = float("-inf")
            bestAction = Directions.STOP
            depth -= 1
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                minResult = minAction(successor, depth, 1)[0]
                if v < minResult:
                    v = minResult
                    bestAction = action
            return (v, bestAction)

        return maxAction(gameState, self.depth, 0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def minValue(gameState, depth, agentIndex, alpha, beta):
            if depth < 0 or gameState.isLose() or gameState.isWin():
                return (self.evaluationFunction(gameState), Directions.STOP)
            v = float("inf")
            worstAction = Directions.STOP
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex != gameState.getNumAgents() - 1:
                    result = minValue(successor, depth,
                                      agentIndex + 1, alpha, beta)[0]
                    if v > result:
                        v = result
                        worstAction = action
                    if v < alpha:
                        return (v, action)
                    beta = min(beta, v)
                else:
                    result = maxValue(
                        successor, depth, 0, alpha, beta)[0]
                    if v > result:
                        v = result
                        worstAction = action
                    if v < alpha:
                        return (v, action)
                    beta = min(beta, v)
            return (v, worstAction)

        def maxValue(gameState, depth, agentIndex, alpha, beta):
            if depth <= 0 or gameState.isLose() or gameState.isWin():
                return (self.evaluationFunction(gameState), Directions.STOP)
            v = float('-inf')
            depth -= 1
            bestAction = Directions.STOP
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                result = minValue(successor, depth, 1, alpha, beta)[0]
                if v < result:
                    v = result
                    bestAction = action
                if v > beta:
                    return (v, bestAction)
                alpha = max(alpha, v)
            return (v, bestAction)
        return maxValue(gameState, self.depth, 0, float('-inf'), float('inf'))[1]


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

        def maxValue(gameState, depth):
            if depth <= 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            v = float("-inf")
            bestAction = Directions.STOP
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                v = max(v, expValue(successor, depth, 1))
            return v

        def expValue(gameState, depth, agentIndex):
            if depth <= 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            v = 0
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex != gameState.getNumAgents() - 1:
                    v += expValue(successor, depth, agentIndex + 1)
                else:
                    v += maxValue(successor, depth - 1)
            return v / len(gameState.getLegalActions(agentIndex))

        bestAction = Directions.STOP
        v = float('-inf')
        agent_index = 0
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            old_v = v
            v = max(v, expValue(successor, self.depth, agent_index + 1))
            if v > old_v:
                bestAction = action
        return bestAction


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This was just copying and pasting our answer from Q1
    ALl the evaluation function does is it increases the evaluation the closer 
    the pacman is to the nearest food. The for loop that loops over newGhostStates
    is intended to increase the evaluation if there is a scared ghost that the pacman
    can reach before the time runs out.
    """

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [
        ghostState.scaredTimer for ghostState in newGhostStates]
    totalScore = 0.0
    for i in range(len(newGhostStates)):
        if newScaredTimes[i] >= manhattanDistance(newGhostStates[i].getPosition(), newPos):
            totalScore += 200
    x, y = newPos
    foodValues = currentGameState.getFood()
    distToFood = 0
    if not newFood.asList():
        distToFood = 1
    else:
        distToFood = 1 / min([manhattanDistance(newPos, foodPos)
                              for foodPos in newFood.asList()])
    return currentGameState.getScore() + distToFood


# Abbreviation
better = betterEvaluationFunction
