''' Daniel Chai, Etai Liokumovich
    Wicked Problem A: Avoiding World War
    Completed'''

import random  # imports random for the probabilities

# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "AvoidingWorldWar"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Daniel Chai', 'Etai Liokumovich']
PROBLEM_CREATION_DATE = "25-APR-2017"
PROBLEM_DESC = \
    '''This formulation of the World War uses generic
Python 3 constructs and has been tested with Python 3.6.'''

# </METADATA>

# <COMMON_CODE>
REMOVAL_POSSIBILITIES = [60, 65, 70, 75, 80, 85, 87, 89, 90]  # Chances of countries removing their nuclear weapons
                                                              # We thought that superpowers are less likely to get rid of theirs

# Determines whether a country will remove their weapon.
def can_remove(s, x):
    '''Tests whether it's legal to move a piece in state s
     from the From location to the To location.'''
    temp = random.randint(0, 99)
    if s.l[x] == 0:
        return False
    return temp < REMOVAL_POSSIBILITIES[x]


# remove random number of weapons from a single country
def remove(s, x):
    REMOVAL_NUMBER = random.randint(0, 300)  # 300 in order make the search go faster.
                                           # Lower the number in order to see more possibilities.
    news = s.__copy__()  # start with a deep copy.
    if REMOVAL_NUMBER > s.l[x]:
        news.l[x] = 0
    else:
        news.l[x] -= REMOVAL_NUMBER
    return news  # return new state


# Determines whether a country can remove all of its weapons
def can_remove_all(s, x):
    if s.l[x] == 0:
        return False
    count = 99999
    for n in range(9):
        if s.l[n] == 0:
            count = count // 10  # chance will increase by 10 times for each country that removed all of its arsenals.
    temp = random.randint(0, count)
    return temp == 0  # 0.001% initial chance that one country will remove everything


# Removes all the weapons from a single country
def remove_all(s, x):
    news = s.__copy__()
    news.l[x] = 0
    return news


# Determines whether all the countries will remove all of their weapons
def can_all_remove(s):
    n = random.randint(0, 999999999)  # 0.000000001% chance that everyone will remove everything.
    return n == 1


# Removing all the weapons
def all_remove(s):
    news = s.__copy__()
    for x in range(9):
        news.l[x] = 0
    return news


def goal_test(s):
    '''If the list is same as Goal state, then it is goal state.'''
    return s.l == [0, 0, 0, 0, 0, 0, 0, 0, 0]


def goal_message():
    return ''' __          ________       __      ______ _____ _____  ______ _____   __          ______  _____  _      _____   __          __     _____  _ 
 \ \        / /  ____|     /\ \    / / __ \_   _|  __ \|  ____|  __ \  \ \        / / __ \|  __ \| |    |  __ \  \ \        / /\   |  __ \| |
  \ \  /\  / /| |__       /  \ \  / / |  | || | | |  | | |__  | |  | |  \ \  /\  / / |  | | |__) | |    | |  | |  \ \  /\  / /  \  | |__) | |
   \ \/  \/ / |  __|     / /\ \ \/ /| |  | || | | |  | |  __| | |  | |   \ \/  \/ /| |  | |  _  /| |    | |  | |   \ \/  \/ / /\ \ |  _  /| |
    \  /\  /  | |____   / ____ \  / | |__| || |_| |__| | |____| |__| |    \  /\  / | |__| | | \ \| |____| |__| |    \  /\  / ____ \| | \ \|_|
     \/  \/   |______| /_/    \_\/   \____/_____|_____/|______|_____/      \/  \/   \____/|_|  \_\______|_____/      \/  \/_/    \_\_|  \_(_)
   _____ ____  _   _  _____ _____         _______ _    _ _            _______ _____ ____  _   _  _____ _ 
  / ____/ __ \| \ | |/ ____|  __ \     /\|__   __| |  | | |        /\|__   __|_   _/ __ \| \ | |/ ____| |
 | |   | |  | |  \| | |  __| |__) |   /  \  | |  | |  | | |       /  \  | |    | || |  | |  \| | (___ | |
 | |   | |  | | . ` | | |_ |  _  /   / /\ \ | |  | |  | | |      / /\ \ | |    | || |  | | . ` |\___ \| |
 | |___| |__| | |\  | |__| | | \ \  / ____ \| |  | |__| | |____ / ____ \| |   _| || |__| | |\  |____) |_|
  \_____\____/|_| \_|\_____|_|  \_\/_/    \_\_|   \____/|______/_/    \_\_|  |_____\____/|_| \_|_____/(_)
                                                                                                         '''


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

# The heuristic function
def h_custom(s):
    sum = 0
    for x in s.l:
        sum += x
    return sum * sum   # We chose sum^2 because we thought that more weapons means harder removal

# </COMMON_CODE>

# <STATE>
class State():
    def __init__(self, l, f):
        self.l = l
        self.f = f

    def __str__(self):
        string = ""
        for x in range(9):
            string += COUNTRIES[x] + ": " + str(self.l[x]) + "\n"
        return string

    def __eq__(self, s2):
        sum1 = 0
        sum2 = 0
        for x in self.l:
            sum1 += x
        if (type(s2) == State):
            for y in s2.l:
                sum2 += y
        else:
            return False
        return sum1 == sum2

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([], 0)
        for x in self.l:
            news.l.append(x)
        return news

    def __lt__(self, other):
        sum1 = 0
        sum2 = 0
        for x in self.l:
            sum1 += x
        for y in other.l:
            sum2 += y
        return sum1 < sum2


# </STATE>
COUNTRIES = ["Russia", "US", "Israel", "France", "China", "UK", "Pakistan", "India", "NK"]
# <OPERATORS>
# What are the ways of removing nuclear weapons
# Ways:
#   1) Everyone decides to remove some number of weapons.
#   2) A country decides to remove all of its weapons.
#   3) Everyone decides to completely remove all the weapons.
OPERATORS = []
for x in range(9):
    OPERATORS += [Operator("Everyone decided to remove some weapons.",
                           lambda s, country=x: can_remove(s, country),
                           lambda s, country=x: remove(s, country)),
                  Operator(COUNTRIES[x] + " has decided to remove all their arsenal.",
                           lambda s, country=x: can_remove_all(s, country),
                           lambda s, country=x: remove_all(s, country)),
                  Operator("Everyone decided to completely remove all their weapons",
                           lambda s: can_all_remove(s),
                           lambda s: all_remove(s))]

# </OPERATORS>

# <INITIAL_STATE>

INITIAL_STATE = State([7300, 6900, 400, 300, 260, 215, 130, 120, 10], 0)
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
# </INITIAL_STATE>

# <GOAL TEST>
GOAL_TEST = lambda s: goal_test(s)
# </GOAL TEST>

# <GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message()
# </GOAL_MESSAGE_FUNCTION>

# <HEURISTICS>
HEURISTICS = {'h_custom': h_custom}
# </HEURISTICS>
