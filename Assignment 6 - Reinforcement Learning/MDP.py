'''MDP.py
S. Tanimoto, May 2016, 2017.

Provides representations for Markov Decision Processes, plus
functionality for running the transitions.

The transition function should be a function of three arguments:
T(s, a, sp), where s and sp are states and a is an action.
The reward function should also be a function of the three same
arguments.  However, its return value is not a probability but
a numeric reward value -- any real number.

operators:  state-space search objects consisting of a precondition
 and deterministic state-transformation function.
 We assume these are in the "QUIET" format used in earlier assignments.

actions:  objects (for us just Python strings) that are 
 stochastically mapped into operators at runtime according 
 to the Transition function.


CSE 415 STUDENTS: Implement the 3 methods indicated near the
end of this file.

'''
import random

REPORTING = True


class MDP:
    def __init__(self):
        self.known_states = set()
        self.succ = {}  # hash of adjacency lists by state.

    def register_start_state(self, start_state):
        self.start_state = start_state
        self.known_states.add(start_state)

    def register_actions(self, action_list):
        self.actions = action_list

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function

    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        neighbors = self.succ.get(state, False)
        if neighbors == False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            self.succ[state] = neighbors
            self.known_states.update(neighbors)
        return neighbors

    def random_episode(self, nsteps):
        self.current_state = self.start_state
        self.known_states = set()
        self.known_states.add(self.current_state)
        self.current_reward = 0.0
        for i in range(nsteps):
            self.take_action(random.choice(self.actions))
            if self.current_state == 'DEAD':
                print('Terminating at DEAD state.')
                break
        if REPORTING: print("Done with " + str(i) + " of random exploration.")

    def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = self.R(s, a, s)
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold > rnd:
                r = self.R(s, a, sp)
                s = sp
                break
        self.current_state = s
        self.known_states.add(self.current_state)
        if REPORTING: print("After action " + a + ", moving to state " + str(self.current_state) + \
                            "; reward is " + str(r))

    # Takes in self as a parameter
    # Sets known_states to set of all states
    # Does not return anything
    def generateAllStates(self):
        s = self.start_state
        OPEN = [s]
        CLOSED = []

        while OPEN:
            S = OPEN[0]
            del OPEN[0]
            CLOSED.append(S)
            L = []
            for neighbors in self.state_neighbors(S):
                if neighbors not in OPEN and neighbors not in CLOSED:
                    L.append(neighbors)
                    # print("neighbors: " + str(neighbors))
            OPEN = L + OPEN
        self.known_states.update(CLOSED)

    # Takes self, discount factor, and number of iterations as parameters
    # Calculates value of each state after nth iteration
    # returns nothing
    def valueIteration(self, discount, iterations):
        self.V = {}
        new_V = {}
        for states in self.known_states:
            self.V[states] = 0  # Initialize all the states' values to 0
            new_V[states] = 0
        while iterations > 0:
            for S in self.V.keys():  # For every key
                values = []
                for action in self.actions:  # For every action
                    value = 0
                    for op in self.ops:  # Look at all the possible moves
                        if op.is_applicable(S):
                            new_state = op.apply(S)
                            R = self.R(S, action, new_state)
                            T = self.T(S, action, new_state)
                            prev = self.V[new_state]
                            num = T * (R + (discount * prev))  # Calculate the V value
                            value += num

                    # When the state stays still
                    T = self.T(S, action, S)
                    num = T * (discount * self.V[S])
                    value += num
                    values.append(value)
                best = 0
                if values:
                    best = max(values)
                new_V[S] = best
            self.V.update(new_V)
            iterations -= 1

    # Takes discount, nEpisode, epsilon as parameters
    # Calculates the Qvalue
    def QLearning(self, discount, nEpisodes, epsilon):
        self.Q = {}
        self.new_Q = {}
        N = {}
        for state in self.known_states:
            for action_name in self.actions:
                self.Q[(state, action_name)] = 0
                self.new_Q[(state, action_name)] = 0
                N[(state, action_name)] = 1
        # while nEpisodes > 0:
        #     current_state = self.start_state
        #     while current_state != "DEAD":
        #         # Select the best move
        #         best_action = -1
        #         best_value = -999
        #         for i, action in enumerate(self.actions):
        #             tuple = (current_state, action)
        #             value = self.Q[tuple]
        #             if best_value < value:
        #                 best_action = i
        #                 best_value = value
        #         if best_action == 3:
        #             best_action = 2
        #         elif best_action == 2:
        #             best_action = 3
        #         elif best_action == 1:
        #             best_action = 0
        #         op = self.ops[best_action]
        #         # Select a Random move
        #         if random.random() < epsilon:
        #             op = random.choice(self.ops)
        #
        #         action = op.name.split(" ")[1]
        #         if action == "to":
        #             action = "End"
        #         tuple = (current_state, action)
        #         if op.is_applicable(current_state):
        #             new_state = op.apply(current_state)
        #             R = self.R(current_state, action, new_state)
        #             max_Q = []
        #             for action in self.actions:
        #                 value = self.Q[(new_state, action)]
        #                 max_Q.append(value)
        #             maxQ = max(max_Q)
        #             sample = R + (discount * maxQ)  # Calculate the new sample
        #             old = self.Q[tuple]
        #             alpha = 1 / N[tuple]
        #             self.new_Q[tuple] = ((1 - alpha) * old) + (alpha * sample)
        #             N[tuple] += 1
        #             current_state = new_state
        #     self.Q.update(self.new_Q)
        #     nEpisodes -= 1


        while nEpisodes > 0:
            current_state = self.start_state
            while current_state != "DEAD":
                op = random.choice(self.ops)
                action_name = op.name.split(" ")[1]
                if action_name == "to":
                    action_name = "End"

                # Make the move
                if op.is_applicable(current_state):
                    new_state = op.apply(current_state)
                    max_Q = []
                    for action in self.actions:
                        value = self.Q[(new_state, action)]
                        max_Q.append(value)
                    maxQ = max(max_Q)
                    R = self.R(current_state, action_name, new_state)
                    sample = R + (discount * maxQ)
                    tuple = (current_state, action_name)
                    alpha = 1 / N[tuple]
                    value = ((1 - alpha) * self.Q[tuple]) + (alpha * sample)
                    self.Q[tuple] = value
                    N[tuple] += 1
                    current_state = new_state

            nEpisodes -= 1

    def extractPolicy(self):
        self.optPolicy = {}
        for state in self.known_states:
            best_value = -100000
            for action in self.actions:
                tuple = (state, action)
                value = self.Q[tuple]
                if type(value) == float:
                    if best_value < value:
                        best = action
                        best_value = value
                        self.optPolicy[state] = best
