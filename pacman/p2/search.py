# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState(
  """
  "*** YOUR CODE HERE ***"
  
  from game import Directions
  from game import Grid
  n = Directions.NORTH
  s = Directions.SOUTH
  e = Directions.EAST
  w = Directions.WEST
  
#  print "Start:", problem.getStartState()
#  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#  print "Start's successors:", problem.getSuccessors(problem.getStartState())

#  for i in range(35):
#    for j in range(35):
#      aLoc = (i,j)
#      if problem.isGoalState(aLoc):
#        print "Goal is ",aLoc
  
  visited = Grid(100,100)
  checkLoc = problem.getStartState()
  
  foundGoal = False
  toBeChecked = util.Stack()

  foundGoal, path = recursiveDFS( problem, checkLoc, toBeChecked, visited )
  return path

def recursiveDFS( problem, checkLoc, toBeChecked, visited):
  x,y = checkLoc
  
#  print "Now serving [",x,y,"]"
  if visited[x][y]:
#    print "Been here done that."
    return False,None

  visited[x][y] = True

  if problem.isGoalState(checkLoc):
    foundGoal = True
#    print "Yippee we're done!!"
    return foundGoal,None

#  print "checkLoc =",checkLoc
  nextStep = problem.getSuccessors(checkLoc)
  if len(nextStep)==1:
	return False,None

#  print "nextStep =",nextStep 
#  if nextStep[0] == None:
#    print "No next steps from here."
#    return False,None

  for eachStep in nextStep:
    foundGoal, finishPath = recursiveDFS(problem, eachStep[0], toBeChecked, visited)
    if foundGoal:
#      print eachStep
#      util.raiseNotDefined()
      if finishPath == None:
        nextPathStep = [eachStep[1]]
      else:
        nextPathStep = [eachStep[1]] + finishPath    
#      print "Found the goal",nextPathStep
      return foundGoal,nextPathStep

  return False, None


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from game import Grid

  #print "Start:", problem.getStartState()
  #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  #print "BFS Start's successors:", problem.getSuccessors(problem.getStartState())
  start = problem.getStartState()
  x = start[0]
  if type(x)== tuple:
    print "Corner Problem State Detected"
    cornerState = True
  else:
    print "Normal State Detected"
    cornerState = False

  queue = util.Queue()
  fstate = ((problem.getStartState(),"",0), [], 0)
  queue.push(fstate)
  visited = Grid(100,100)

  while True:
    if queue.isEmpty():
      return None
    
    fstate = queue.pop()
    step = fstate[0]

    #print "fstate=",fstate
    #print "step=",step

    if problem.isGoalState(step[0]):
      #print "Found It"
      if cornerState:
	problem.satisfyGoal(step[0])
	myFlag=(step[0])[1]
	fstate2 = ((step[0], "",0), fstate[1],fstate[2])
	queue = util.Queue()
	queue.push(fstate2)
	visited=Grid(100,100)
	
	if not True in myFlag:
		print "All Done"
		return fstate[1]
      else:
        return fstate[1]
    else:
      next = problem.getSuccessors(step[0])
      for each in next:
	if cornerState:
	  cornerLoc = each[0]
	  x,y = cornerLoc[0]
	else:
	  x,y = each[0]

        #print "Now serving [",x,y,"]"
        if visited[x][y]:
          l = 0
          #print "Been here done that."
        else:
          visited[x][y] = True
          #print "adding an each.  fstate before=", fstate[1]
          saveState = []
          saveState.extend(fstate[1])
          saveState.append(each[1])
          pathSize = fstate[2] +1
          xstate = (each,saveState,pathSize)
          queue.push(xstate)
# end while loop
  
#  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from game import Grid

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  start = problem.getStartState()
  x = start[0]
  if type(x)== tuple:
    print "Corner Problem State Detected"
    cornerState = True
  else:
    print "Normal State Detected"
    cornerState = False

  queue = util.PriorityQueue()
  fstate = ((problem.getStartState(),"",0), [], 0)
  queue.push(fstate,0)
  visited = Grid(100,100)

  while True:
    if queue.isEmpty():
      return None
    
    fstate = queue.pop()
    step = fstate[0]

    #print "fstate=",fstate
    #print "step=",step

    if problem.isGoalState(step[0]):
      #print "Found It"
      if cornerState:
	problem.satisfyGoal(step[0])
	myFlag=(step[0])[1]
	fstate2 = ((step[0], "",0), fstate[1],fstate[2])
	queue = util.PriorityQueue()
	queue.push(fstate2,0)
	visited=Grid(100,100)
	
	if not (True in myFlag):
	  print "All Done"
	  return fstate[1]
      else:
        return fstate[1]
    else:
      next = problem.getSuccessors(step[0])
      for each in next:
	if cornerState:
	  cornerLoc = each[0]
	  x,y = cornerLoc[0]
	else:
	  x,y = each[0]
        #print "Now serving [",x,y,"]"
        if visited[x][y]:
          l = 0
          #print "Been here done that."
        else:
          visited[x][y] = True
          #print "adding an each.  fstate before=", fstate[1]
          saveState = []
          saveState.extend(fstate[1])
          saveState.append(each[1])
          pathSize = fstate[2] +each[2]
          xstate = (each,saveState,pathSize)
          queue.push(xstate, pathSize)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Grid

  #print "Start:", problem.getStartState()
  #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  #print "Start's successors:", problem.getSuccessors(problem.getStartState())
  start = problem.getStartState()
  x = start[0]
  test = Grid(2,2)
  #print start, type(start[1])
  if type(x)== tuple:
    if type(start[1]) == type(test):
      print "A* Food Problem State Detected"
      foodState = True
      cornerState = False
      print "start[1]=",start[1]
      food2go = start[1].count()
      print "food2go =", food2go
    else:
      print "A* Corner Problem State Detected"
      cornerState = True
      foodState = False
  else:
    print "A* Normal State Detected"
    cornerState = False
    foodState = False

  queue = util.PriorityQueue()
  fstate = ((problem.getStartState(),"",0), [], 0)
  queue.push(fstate,0)
  visited = Grid(100,100)

  while True:
    if queue.isEmpty():
      print "Ran out of ideas"
      return fstate[1]
    
    fstate = queue.pop()
    step = fstate[0]

    #print "fstate=",fstate
    #print "step=",step

    if problem.isGoalState(step[0]):
      print "Found It"
      if cornerState:
	problem.satisfyGoal(step[0])
	myFlag=(step[0])[1]
	fstate2 = ((step[0], "",0), fstate[1],fstate[2])
	queue = util.PriorityQueue()
	queue.push(fstate2,0)
	visited=Grid(100,100)
	
	if not (True in myFlag):
		print "All Done"
		return fstate[1]
      else:
        return fstate[1]
    else:
      if foodState:
        #print "Step =", step
        aLoc = step[0]
        x,y = aLoc[0]
        food = aLoc[1]
        myFood = food.count()
        #if myFood < food2go:
	if food[x][y]:        
	  #print "Food = Yum"
          food2go = myFood
          fstate2 = ((step[0], "",0), fstate[1],fstate[2])
	  queue = util.PriorityQueue()
	  #queue.push(fstate2,0)
	  visited=Grid(100,100)
          #visited[x][y]=True
                
      next = problem.getSuccessors(step[0])
      for each in next:
	if cornerState or foodState:
	  cornerLoc = each[0]
	  x,y = cornerLoc[0]
	else:
	  x,y = each[0]
        #print "Now serving [",x,y,"]"
        if (visited[x][y]):
          l = 0
          print "Been here done that."
        else:
	    visited[x][y] = True
            print "adding an each.  fstate before=", fstate[1]
            saveState = []
            saveState.extend(fstate[1])
            saveState.append(each[1])
            move = each[1]
            loc = each[0]
            #print "fstate for heuristic =",saveState
            #print "move for heuristic=",move
            #print "loc for heuristic=",loc
            priority = heuristic(loc, problem)
            #print "Priority=", priority, loc
            pathSize = fstate[2] +1
            xstate = []
            xstate = (each,saveState,pathSize)
            #print "xstate in =",xstate
            queue.push(xstate, priority)
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
