# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions() 

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    #print legalMoves[chosenIndex]
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    walls = currentGameState.getWalls()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    score = 0
    x1,y1 = newPos
    ghosts = successorGameState.getGhostPositions()
    for each in ghosts:
	x2,y2 = each
	if ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)) < 9:
		score -= 50*(10-(abs(x1-x2)+abs(y1-y2)))

    oldNumFood=currentGameState.getNumFood()
    newFood=successorGameState.getNumFood()
    if (newFood< oldNumFood):
	score+=10

    food=currentGameState.getFood().asList()
    foodscore= []
    for each in food:
	x2,y2 = each
	foodscore.append(90/(1+abs(x1-x2)+abs(y1-y2)))

    for each in successorGameState.getCapsules():
	x2,y2 = each	
	foodscore.append(50/(1+abs(x1-x2)+abs(y1-y2)))

    score += max(foodscore)
	
    #if action == "Stop":
    #    score -= 10

    x2 = (walls.width/2) -1
    y2 = (walls.height/2) -1
    score -= 20/(1+abs(x1-x2)+abs(y1-y2))
    
    return score

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    topDepth = self.depth
    topMax, topScore = self.getOneAction (topDepth, gameState)
    return topMax
  
  def getOneAction (self, myDepth, gameState):
    numAgents = gameState.getNumAgents()
    actions0 = gameState.getLegalActions(0)
    MAX = Directions.STOP
    MIN = Directions.STOP
    maxScore = []
    minScore = []
    total = -999
    max2Score = -999
    maxScore.append(max2Score)
    for each0 in actions0:
      max2Score = -999
      if each0 == "Stop":
        "*** ignore Stop as an option. Change Stop to anything to disable ***"
        max2Score += 0
      else:
    	nextState = gameState.generateSuccessor(0,each0)
    	"*** check out options for this state, unless depth limit reached or game over ***"
    	if (myDepth > 1):
          MAX2,max2Score = self.getOneAction((myDepth-1),nextState)

        max3Score = self.evaluationFunction(nextState)
        count = 1
        minScore = []
        while(count<numAgents):
          actions = gameState.getLegalActions(count)
          for each in actions:
            nextState = gameState.generateSuccessor(count,each)
            minScore.append(self.evaluationFunction(nextState))
            if (min(minScore)==self.evaluationFunction(nextState)):
              MIN = each
			
	  count+=1
	  
        max3Score += min(minScore)
        if max3Score > max2Score:
          "*** This node is better than the limbs below it ***"
          max2Score = max3Score
        
	maxScore.append(max2Score)
	if (max(maxScore) == max2Score):
          "*** this is the optimal MAX state (so far) ***"
          MAX = each0
          
    return MAX, max(maxScore)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    topDepth = self.depth
    topMax, topScore = self.getOneAction (topDepth, gameState)
    return topMax
  
  def getOneAction (self, myDepth, gameState):
    numAgents = gameState.getNumAgents()
    actions0 = gameState.getLegalActions(0)
    MAX = Directions.STOP
    MIN = Directions.STOP
    maxScore = []
    minScore = []
    total = -999
    max2Score = -999
    maxScore.append(max2Score)
    for each0 in actions0:
      max2Score = -999
      if each0 == "Stop":
        "*** ignore Stop as an option. Change Stop to anything to disable ***"
        max2Score += 0
      else:
    	nextState = gameState.generateSuccessor(0,each0)
    	if nextState.isLose():
          "*** prune losing limb ***"
          #print ("Loser")
          return each0,-999

        max3Score = self.evaluationFunction(nextState)
        count = 1
        minScore = []
        while(count<numAgents):
          actions = gameState.getLegalActions(count)
          for each in actions:
            nextState = gameState.generateSuccessor(count,each)
            minScore.append(self.evaluationFunction(nextState))
            if (min(minScore)==self.evaluationFunction(nextState)):
              MIN = each
			
	  count+=1
	  
        max3Score += min(minScore)

	if (max(maxScore) <= max3Score):
          "*** this is the optimal MAX state (so far) ***"
          MAX = each0
          "*** check out options for this state, unless depth limit reached or game over ***"
          if (myDepth > 1) & (nextState.getNumFood()>0):
            MAX2,max2Score = self.getOneAction((myDepth-1),nextState)
          
        if max3Score > max2Score:
          "*** This node is better than the limbs below it ***"
          max2Score = max3Score
        
	maxScore.append(max2Score)
    return MAX, max(maxScore)

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
    topDepth = self.depth
    topMax, topScore = self.getOneAction (topDepth, gameState)
    #print ("topmax, topscore", topMax, topScore)
    return topMax
  
  def getOneAction (self, myDepth, gameState):
    numAgents = gameState.getNumAgents()
    actions0 = gameState.getLegalActions(0)
    MAX = Directions.STOP
    MIN = Directions.STOP
    maxScore = []
    minScore = []
    total = -999
    max3Score=0
    max2Score = -999
    maxScore.append(max2Score)
    for each0 in actions0:
      max2Score = -999
      if each0 == "StopGaTech":
        "*** ignore Stop as an option. Change Stop to anything to disable ***"
        max2Score += 0
      else:
    	nextState = gameState.generateSuccessor(0,each0)
    	if nextState.isLose():
          "*** prune losing limb ***"
          #print ("Loser")
        else:
          
          "*** check out options for this state, unless depth limit reached or game over ***"
          if (myDepth > 1)& (nextState.getNumFood()>0):
            MAX2,max2Score = self.getOneAction((myDepth-1),nextState)

          max3Score = self.evaluationFunction(nextState)
          #print ("Loc,Val=",nextState.getPacmanPosition(),max3Score)

          needMin = False
          x1,y1 = nextState.getPacmanPosition()
          ghosts = nextState.getGhostPositions()
          for eachGhost in ghosts:
            x2,y2 = eachGhost
            if (abs(x1-x2)+abs(y1-y2)) < 2:
              needMin = True

          if needMin:
            "*** Is there a Ghost nearby? ***"
            count = 1
            minScore = []
            while(count<numAgents):
              actions = gameState.getLegalActions(count)
              for each in actions:
                nextState = gameState.generateSuccessor(count,each)
                minScore.append(self.evaluationFunction(nextState))
                if (min(minScore)==self.evaluationFunction(nextState)):
                  MIN = each
			
              count+=1
	  
            max3Score += min(minScore)
          else:
            max3Score += max3Score
          
          if max3Score > max2Score:
            "*** This node is better than the limbs below it ***"
            max2Score = max3Score
        
          maxScore.append(max2Score)
          if (max(maxScore) == max2Score):
            "*** this is the optimal MAX state (so far) ***"
            MAX = each0
          
    return MAX, max(maxScore)


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <Score is adjusted by:
				+ distance from food
				+ distance from capsules
				- for distance away from ghosts
				
							>
  """
  "*** YOUR CODE HERE ***"
  oldFood = currentGameState.getFood()
  walls = currentGameState.getWalls()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  score = currentGameState.getScore()
  x1,y1 = currentGameState.getPacmanPosition()
  
  #if ghosts are close score is worse for live or better for scared
  newGhostStates = currentGameState.getGhostStates()
  for ghostState in newGhostStates:
    x2,y2 = ghostState.getPosition()
    ghostDist = abs(x1-x2)+abs(y1-y2)
    if ghostState.scaredTimer > ghostDist:
      "*** Eat this Ghost***"
      score += 100/(1+ghostDist)
    elif ghostDist < 9:
      score -= 2000000*(10-ghostDist)
      
  #being near food is good
  food=currentGameState.getFood().asList()
  foodscore= []
  for each in food:
  	x2,y2 = each
  	dist2food=abs(x1-x2)+abs(y1-y2)
  	if (dist2food==0):
          print("ERROR: FOOD HERE!!!!!")
          score += 1000000
        else:
          foodscore.append(50/(dist2food))

  # being near capsules is good
  for each in currentGameState.getCapsules():
  	x2,y2 = each	
  	foodscore.append(2000/(1+abs(x1-x2)+abs(y1-y2)))

  if (len(foodscore)!=0):
    score += max(foodscore)

  x2 = (walls.width/2) -1
  y2 = (walls.height/2) -1
  score -= 1/5*(1+abs(x1-x2)+abs(y1-y2)) #stay away from middle (better ghost avoidance)

  if currentGameState.isLose():
    score = -9999
    
  return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    topDepth = 5
    topMax, topScore = self.getOneAction (topDepth, gameState)
    #print ("topmax, topscore", topMax, topScore)
    return topMax
  
  def getOneAction (self, myDepth, gameState):
    numAgents = gameState.getNumAgents()
    actions0 = gameState.getLegalActions(0)
    MAX = Directions.STOP
    MIN = Directions.STOP
    maxScore = []
    minScore = []
    total = -999
    max3Score=0
    max2Score = -999
    maxScore.append(max2Score)
    for each0 in actions0:
      max2Score = -999
      if each0 == "StopGaTech":
        "*** ignore Stop as an option. Change Stop to anything to disable ***"
        max2Score += 0
      else:
    	nextState = gameState.generateSuccessor(0,each0)
    	if nextState.isLose():
          "*** prune losing limb ***"
          #print ("Loser")
        else:
          
          "*** check out options for this state, unless depth limit reached or game over ***"
          if (myDepth > 0)& (nextState.getNumFood()>0):
            MAX2,max2Score = self.getOneAction((myDepth-1),nextState)

          max3Score = self.evaluationFunction(nextState)
          #print ("Loc,Val=",nextState.getPacmanPosition(),max3Score)

          needMin = False
          x1,y1 = nextState.getPacmanPosition()
          ghosts = nextState.getGhostPositions()
          for eachGhost in ghosts:
            x2,y2 = eachGhost
            if (abs(x1-x2)+abs(y1-y2)) < self.depth:
              needMin = True

          if needMin:
            "*** Is there a Ghost nearby? ***"
            count = 1
            minScore = []
            while(count<numAgents):
              actions = gameState.getLegalActions(count)
              for each in actions:
                nextState = gameState.generateSuccessor(count,each)
                minScore.append(self.evaluationFunction(nextState))
                if (min(minScore)==self.evaluationFunction(nextState)):
                  MIN = each
			
              count+=1
	  
            max3Score += min(minScore)
          else:
            max3Score += max3Score
          
          if max3Score > max2Score:
            "*** This node is better than the limbs below it ***"
            max2Score = max3Score
        
          maxScore.append(max2Score)
          if (max(maxScore) == max2Score):
            "*** this is the optimal MAX state (so far) ***"
            MAX = each0
          
    return MAX, max(maxScore)

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
        
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <Score is adjusted by:
				+ distance from food
				+ distance from capsules
				- for distance away from ghosts
				
							>
    """
    "*** YOUR CODE HERE ***"
    oldFood = currentGameState.getFood()
    walls = currentGameState.getWalls()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore()
    x1,y1 = currentGameState.getPacmanPosition()
  
    #if ghosts are close score is worse for live or better for scared
    newGhostStates = currentGameState.getGhostStates()
    for ghostState in newGhostStates:
      x2,y2 = ghostState.getPosition()
      ghostDist = abs(x1-x2)+abs(y1-y2)
      if ghostState.scaredTimer > ghostDist:
        "*** Eat this Ghost***"
        score += 100/(1+ghostDist)
      elif ghostDist < 9:
        score -= 2000000*(10-ghostDist)
      
    #being near food is good
    food=currentGameState.getFood().asList()
    foodscore= []
    for each in food:
    	x2,y2 = each
    	dist2food=abs(x1-x2)+abs(y1-y2)
    	if (dist2food==0):
            print("ERROR: FOOD HERE!!!!!")
            score += 1000000
        else:
            foodscore.append(50/(dist2food))

    # being near capsules is good
    for each in currentGameState.getCapsules():
    	x2,y2 = each	
  	foodscore.append(2000/(1+abs(x1-x2)+abs(y1-y2)))

    if (len(foodscore)!=0):
      score += max(foodscore)

    x2 = (walls.width/2) -1
    y2 = (walls.height/2) -1
    score -= 1/5*(1+abs(x1-x2)+abs(y1-y2)) #stay away from middle (better ghost avoidance)

    if currentGameState.isLose():
      score = -9999
    
    return score

