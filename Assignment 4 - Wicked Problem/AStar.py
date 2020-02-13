''' Daniel Chai, CSE 415, April 18th 2017
    1532825'''
#  Astar.py, April 2017
# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from queue import PriorityQueue
import heapq

# DO NOT CHANGE THIS SECTION 
if sys.argv==[''] or len(sys.argv)<2:
    import AvoidWar as Problem
    #heuristics = lambda s: Problem.HEURISTICS['h_hamming'](s)
    #heuristics = lambda s: Problem.HEURISTICS['h_euclidean'](s)
    #heuristics = lambda s: Problem.HEURISTICS['h_manhattan'](s)
    heuristics = lambda s: Problem.HEURISTICS['h_custom'](s)
    
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into 
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQueue()
    OPEN.put(initial_state, 0)
    OpenList = [initial_state]
    CLOSED = []
    BACKLINKS[initial_state] = -1
    COST = {}
    COST[initial_state] = 0

    while not OPEN.empty():
        S = OPEN.get()
        while S in CLOSED:
            S = OPEN.get()
        CLOSED.append(S)
        
        # DO NOT CHANGE THIS SECTION: beginning
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        COUNT += 1
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(OPEN.qsize()))
                print("len(CLOSED)=" + str(len(CLOSED)))
        for op in Problem.OPERATORS:  # For every successor:
            if op.precond(S):         # if the move is legal to make:
                new_state = op.state_transf(S)   # set new_state
                new_cost = COST[S] + 1           # set new_state's cost
                if new_state not in OpenList or new_state not in CLOSED:  # if the new state has never been seen before
                    COST[new_state] = new_cost  # store the cost of the new_state
                    new_state.f = new_cost + heuristics(new_state)  # set new_state's f value
                    BACKLINKS[new_state] = S  # set new_state's parent
                    OPEN.put(new_state, new_state.f)  # put new_state into open
                    OpenList.append(new_state)  # just for existence
                else:  # if new_state has been seen before
                    if new_state in BACKLINKS: # if the parent exists
                        temp = new_state.f + COST[S]  # set temp to the new cost
                    else:
                        temp = new_state.f  # set temp to old f value
                    if temp < new_state.f:  # if the new cost is lower
                        COST[new_state] = COST[new_state] - new_state.f + temp  # store the new value
                        new_state.f = temp
                        if new_state in OpenList:  #
                            OPEN.remove(new_state)
                            heapq.heapify(OPEN)
                            OPEN.put(new_state, new_state.f)
                            OpenList.append(new_state)
                        if new_state in CLOSED:
                            OPEN.put(new_state, new_state.f)
                            CLOSED.remove(new_state)

    print("Error: No path found")


# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path    

if __name__=='__main__':
    path, name = runAStar()

