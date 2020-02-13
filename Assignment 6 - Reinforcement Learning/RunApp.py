'''RunApp.py

This program imports Grid.py and MDP.py and runs certain algorithms to
demonstrate aspects of reinforcement learning.

CSE 415  Students: Fill in the missing code where indicated.

'''

import MDP
import Grid_updated as Grid

def GW_Values_string(V_dict):
    grid_world = [[0, 0, 0, 0] for r in range(3)]
    for state in V_dict:
        if state != "DEAD":
            y = state[0]
            x = 2 - state[1]
            grid_world[x][y] = V_dict[state]
    s = ''
    for x in range(3):
        for y in range(4):
            s += "[" + '%.3f' % round(grid_world[x][y], 3) + "] "
        s += "\n"
    return s

def GW_QValues_string(Q_dict):
    grid_world = [[[],[],[],[]] for r in range(3)]
    for tuple in Q_dict:
        state = tuple[0]
        action = tuple[1]
        if state != "DEAD":
            y = state[0]
            x = 2 - state[1]
            grid_world[x][y].append([action, Q_dict[tuple]])
    s = ''
    for x in range(3):
        for y in range(4):
            s += "(" + str(y) + ", " + str(2 - x) + ")"
            for list in grid_world[x][y]:
                if list == 0:
                    s += "[boulder] "
                elif type(list[1]) == int:
                    s += "[" + list[0][:1] + ": " + str(list[1])+ "] "
                else:
                    s += "[" + list[0][:1] + ": " + '%.3f' % round(list[1], 3) + "] "
        s += "\n"
    return s

def GW_Policy_string(optPolicy):
    grid_world = [[0, 0, 0, 0] for r in range(3)]
    for state in optPolicy:
        if state != "DEAD":
            y = state[0]
            x = 2 - state[1]
            grid_world[x][y] = optPolicy[state]
    s = ''
    for x in range(3):
        for y in range(4):
            s += "[" + str(grid_world[x][y]) + "] "
        s += "\n"
    return s



def test():
    '''Create the MDP, then run an episode of random actions for 10 steps.'''
    grid_MDP = MDP.MDP()
    grid_MDP.register_start_state((0,0))
    grid_MDP.register_actions(Grid.ACTIONS)
    grid_MDP.register_operators(Grid.OPERATORS)
    grid_MDP.register_transition_function(Grid.T)
    grid_MDP.register_reward_function(Grid.R)
    #grid_MDP.random_episode(100)
    grid_MDP.generateAllStates()

    # Uncomment the following, when you are ready...

    grid_MDP.valueIteration(0.9, 6)
    print(GW_Values_string(grid_MDP.V))

    grid_MDP.QLearning(0.1, 2, 0.1)
    print(GW_QValues_string(grid_MDP.Q))

    grid_MDP.extractPolicy()
    print(GW_Policy_string(grid_MDP.optPolicy))

test()
