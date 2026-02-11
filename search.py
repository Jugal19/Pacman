

# search.py
# Assignment 1:
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE *** (Q1)"
    
    # Initialize the fringe using a Stack (LIFO) for DFS
    # The fringe will store tuples of (state, path_to_state)
    fringe = util.Stack()
    
    # Keep track of visited states to avoid cycles
    visited = set()
    
    # Get the starting state from the problem
    start_state = problem.getStartState()
    
    # Push the initial state onto the fringe with an empty path
    fringe.push((start_state, []))
    
    # Continue searching while there are states in the fringe
    while not fringe.isEmpty():
        # Pop a state and its associated path from the fringe
        current_state, path = fringe.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(current_state):
            return path
        
        # Only explore states we haven't visited yet
        if current_state not in visited:
            # Mark this state as visited
            visited.add(current_state)
            
            # Get all successors of the current state
            # Each successor is a tuple: (next_state, action, cost)
            successors = problem.getSuccessors(current_state)
            
            # Add each successor to the fringe
            for next_state, action, cost in successors:
                if next_state not in visited:
                    # Create a new path that includes the action to reach next_state
                    new_path = path + [action]
                    fringe.push((next_state, new_path))
    
    # If we exit the loop without finding a goal, return empty list
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    
    "*** YOUR CODE HERE *** (Q2)"
    
    # Initialize the fringe using a Queue (FIFO) for BFS
    # The fringe will store tuples of (state, path_to_state)
    fringe = util.Queue()
    
    # Keep track of visited states to avoid exploring the same state multiple times
    visited = set()
    
    # Get the starting state from the problem
    start_state = problem.getStartState()
    
    # Push the initial state onto the fringe with an empty path
    fringe.push((start_state, []))
    
    # Mark the start state as visited right away to prevent re-expansion
    visited.add(start_state)
    
    # Continue searching while there are states in the fringe
    while not fringe.isEmpty():
        # Pop a state and its associated path from the fringe
        current_state, path = fringe.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(current_state):
            return path
        
        # Get all successors of the current state
        # Each successor is a tuple: (next_state, action, cost)
        successors = problem.getSuccessors(current_state)
        
        # Add each unvisited successor to the fringe
        for next_state, action, cost in successors:
            if next_state not in visited:
                # Mark as visited when we add to fringe (important for BFS)
                visited.add(next_state)
                # Create a new path that includes the action to reach next_state
                new_path = path + [action]
                fringe.push((next_state, new_path))
    
    # If we exit the loop without finding a goal, return empty list
    return []

def uniformCostSearch(problem: SearchProblem):
    pq = util.PriorityQueue()
    start = problem.getStartState()

    # best cost to reach each state found so far
    best = {start: 0}

    pq.push((start, []), 0)

    while not pq.isEmpty():
        state, path = pq.pop()
        cost_so_far = best[state]

        if problem.isGoalState(state):
            return path

        for succ, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost

            # only keep it if it's better than what we've already seen
            if succ not in best or new_cost < best[succ]:
                best[succ] = new_cost
                pq.push((succ, path + [action]), new_cost)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    pq = util.PriorityQueue()
    start = problem.getStartState()

    best_g = {start: 0}
    pq.push((start, []), heuristic(start, problem))

    while not pq.isEmpty():
        state, path = pq.pop()
        g = best_g[state]

        if problem.isGoalState(state):
            return path

        for succ, action, step_cost in problem.getSuccessors(state):
            new_g = g + step_cost
            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                f = new_g + heuristic(succ, problem)
                pq.push((succ, path + [action]), f)

    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
