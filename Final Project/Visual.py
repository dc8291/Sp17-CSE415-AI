'''Daniel Chai, CSE 415, May 30th 2017
33-Peg Visualization '''

import QLearning
import Peg
from graphics import *
import operator
import time

def QValues_string(Q_dict):
    x_resolution = 500
    y_resolution = 500
    win = GraphWin("My Window", x_resolution, y_resolution)
    x_interval = x_resolution / 7
    y_interval = y_resolution / 7

    for x in range(7):
        for y in range(7):
            if not (x == 0 and y == 0) and (x < 2 or x > 4) and (y < 2 or y > 4):
                rect = Rectangle(Point(x_interval * y, y_interval * x),
                                 Point(x_interval * (1 + y), y_interval * (1 + x)))
                rect.setFill(color_rgb(153, 255, 153))
                rect.setOutline(color_rgb(0, 0, 0))
                rect.draw(win)


    # Drawing the grid
    for x in range(6):
        line = Line(Point(x_interval * (1 + x), 0), Point(x_interval * (1 + x), y_resolution))
        line.setWidth(5)
        line.draw(win)
    for y in range(6):
        line = Line(Point(0, y_interval * (1 + y)), Point(x_resolution, y_interval * (1 + y)))
        line.setWidth(5)
        line.draw(win)

    sorted_dict = sorted(Q_dict.items(), key=operator.itemgetter(1), reverse = True)
    for state in sorted_dict:
        txt = Text(Point(35, 25), '%.1f' % round(state[1], 1))
        txt.draw(win)
        circles = []
        for x in range(7):
            for y in range(7):
                x_coordinate = (x * x_interval) + (x_interval / 2)
                y_coordinate = (y * y_interval) + (y_interval / 2)
                if state[0].board[x][y] == 1:
                    cir = Circle(Point(x_coordinate, y_coordinate), 15)
                    cir.setFill(color_rgb(255, 100, 50))
                    cir.draw(win)
                    circles.append(cir)

        time.sleep(1)
        for circle in circles:
            circle.undraw()
        txt.undraw()
    win.getMouse()

def test():
    '''Create the MDP, then run an episode of random actions for 10 steps.'''
    initial = Peg.Initial_state
    state = Peg.State(initial)
    learn = QLearning.Q(state)
    learn.register_R(Peg.R)
    learn.register_all_moves(Peg.all_possible_moves)
    learn.register_pegs(Peg.number_of_pegs)

    learn.QLearning(0.9, 100, 0.05)
    print(QValues_string(learn.Q))

test()
