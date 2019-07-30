"""
The base for seach implementations.
"""

import pacai.game
import pacai.search_student
import pacai.util

class SearchProblem(object):
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def startingState(self):
     """
     Returns the start state for the search problem
     """

     pacai.util.raiseNotDefined()

  def isGoal(self, state):
     """
     state: Search state

     Returns True if and only if the state is a valid goal state
     """

     pacai.util.raiseNotDefined()

  def successorStates(self, state):
     """
     state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """

     pacai.util.raiseNotDefined()

  def actionsCost(self, actions):
     """
     actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.
     The sequence must be composed of legal moves.
     """

     pacai.util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.
    For any other maze, the sequence of moves will be incorrect, so only use this for tinyMaze.
    """

    s = pacai.game.Directions.SOUTH
    w = pacai.game.Directions.WEST

    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

# Abbreviations

breadthFirstSearch = pacai.search_student.breadthFirstSearch
bfs = pacai.search_student.breadthFirstSearch

depthFirstSearch = pacai.search_student.depthFirstSearch
dfs = pacai.search_student.depthFirstSearch

aStarSearch = pacai.search_student.aStarSearch
astar = pacai.search_student.aStarSearch

uniformCostSearch = pacai.search_student.uniformCostSearch
ucs = pacai.search_student.uniformCostSearch
