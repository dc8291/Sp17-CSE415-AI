'''Daniel Chai, CSE 415, May 30th 2017
33-Peg puzzle Q learning'''

import random
import operator

class Q:
    def __init__(self, start_state):
        self.start_state = start_state

    def register_R(self, rewards):
        self.R = rewards

    def register_all_moves(self, all_move_function):
        self.all_moves = all_move_function

    def register_pegs(self, peg_function):
        self.number_of_pegs = peg_function

    def choose_move(self, state, epsilon):
        possible_moves = self.all_moves(state)
        result_state = []
        for move in possible_moves:
            new_state = move.apply(state)
            if new_state not in self.Q:
                value = 0
            else:
                value = self.Q[new_state]
            result_state.append((move, value))
        rate = epsilon * 100
        if rate > random.randint(1, 100):
            return random.choice(possible_moves)
        else:
            return max(result_state, key=operator.itemgetter(1))[0]

    def QLearning(self, discount, nEpisodes, epsilon):
        self.Q = {}
        self.new_Q = {}
        N = {}
        self.Q[self.start_state] = 0
        self.new_Q[self.start_state] = 0
        N[self.start_state] = 1

        while nEpisodes > 0:
            current_state = self.start_state

            # Goal state is one peg or no moves
            while self.number_of_pegs(current_state) != 1 and self.all_moves(current_state):
                if current_state not in self.Q:
                    self.Q[current_state] = 0
                    self.new_Q[current_state] = 0
                    N[current_state] = 1
                op = self.choose_move(current_state, epsilon)
                # Make a random move
                new_state = op.apply(current_state)
                max_Q = []
                for actions in self.all_moves(new_state):
                    temp = actions.apply(new_state)
                    if temp not in self.Q:
                        self.Q[temp] = 0
                        self.new_Q[temp] = 0
                        N[temp] = 1
                        value = 0
                    else:
                        value = self.Q[temp]
                    max_Q.append(value)
                if max_Q:
                    maxQ = max(max_Q)
                else:
                    maxQ = 0
                R = self.R(new_state)
                sample = R + (discount * maxQ)
                alpha = 1 / N[current_state]
                value = ((1 - alpha) * self.Q[current_state]) + (alpha * sample)
                self.Q[current_state] = value
                N[current_state] += 1
                current_state = new_state

            nEpisodes -= 1
