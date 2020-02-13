import random
from re import *


def introduce():
    return """My name is Miso, and I sell ramen.
          I was programmed by Daniel Chai.
          If you don't like me, contact him at dc8291@uw.edu
          I like ramen.
          What do you like to eat?"""


def agentName():
    return "Miso"


punctuation_pattern = compile(r"[,.?!;:]")
ramen_factor = False  # "Memory" feature


# noinspection PyTypeChecker,PyTypeChecker
def respond(theInput):
    global ramen_factor
    temp = theInput.lower()
    temp = sub(punctuation_pattern, '', temp)
    wordlist = temp.split(' ')

    if set(['ramen', 'what']).issubset(set(wordlist)):  # When 'ramen' and 'what' is mentioned
        return """Ramen is love.
Visit https://en.wikipedia.org/wiki/Ramen for more info!"""
    if wordlist[0:2] == ['good', 'morning']:  # If input starts with 'good morning'
        return 'Good morning to you too.'
    if wordlist[0] == '':  # Input is empty
        return sample_response()
    if set(['meaning', 'life']).issubset(set(wordlist)):
        return '42'
    if set(['give', 'up']).issubset(set(wordlist)):  # If 'give' 'up' is part of the input
        return """Our greatest weakenss lies in giving up.
The most certain way to succeed is always to try just one more time.
    - Thomas A. Edison"""
    if 'meme' in wordlist or 'memes' in wordlist:  # When 'meme' is mentioned
        return """Any time you try to create an Internet meme, automatic fail.
That's like the worst thing you can do.
    - John Hodgman"""
    if wordlist[0:2] == ['i', 'like']:  # when input starts with 'I like'
        if wordlist[2] == "ramen":
            ramen_factor = True
            return "Really?! You should visit my ramen shop!"
        return "I like " + ' '.join(wordlist[2:]) + " too!"
    if wordlist[0:3] == ['i', 'don\'t', 'like'] or wordlist[0:2] == ['i', 'hate']:  # when input starts with 'I don't like'
        if wordlist[3] == "ramen":
            return "Well, I don't like YOU."
        return "Why don't you like " + ' '.join(wordlist[3:]) + "?"
    if wordlist[0:2] == ['i', 'want'] or wordlist[0:2] == ['i', 'need']:
        # input starts with 'i want' or 'i need'
        if wordlist[2:3] == ['to', 'die']:
            return """Please call 1-800-273-8255 for help.
            Your life matters."""
        return 'Don\'t we all?'
    if ramen_factor:  # If they mentioned they liked ramen
        ramen_factor = False
        return """Wait wait, you mentioned you like ramen, 
what do you like about ramen?"""
    if wpred(wordlist[0]):  # If the input starts with question words
        ending = '?'
        if wpred_response_count == len(wpred_responses):
            ending = '.'
        return wpred_response() + wordlist[0] + ending
    if dpred(wordlist[0]):  # When starting with Auxiliary verb, randomly chooses response.
        return random.choice(dpred_responses)
    if 'because' in wordlist:  # input contains 'because'
        return "That makes sense."
    if 'future' in wordlist:  # input contains 'future'
        return "Why don't we stay in the present?"
    if (True for x in randomwords if x in wordlist):  # input contains 'random words"
        return random_response()
    return sample_response()


sample_responses = ['Please try something else.',
                    'Oops, I don\'t understand',
                    'Tell me how you really feel.',
                    'What does that mean?']
sample_response_count = 0


def sample_response():  # "Cycle" feature for empty inputs
    global sample_response_count
    sample_response_count += 1
    return sample_responses[sample_response_count % len(sample_responses)]


def wpred(w):  # Returns True if w is one of the question words.
    return w in ['when', 'why', 'where', 'how', 'who', 'what']


wpred_responses = ['What do you mean ',
                   'Do we NEED to know '
                   'I\'m not sure ']
wpred_response_count = 0


def wpred_response():
    global wpred_response_count
    wpred_response_count += 1
    return wpred_responses[wpred_response_count % len(wpred_responses)]


#  Acts like a Magic 8 Ball
dpred_responses = ['It is certain.',
                   'It is decidedly so.',
                   'Without a doubt.',
                   'Yes definitely.',
                   'You may rely on it.',
                   'As I see it, yes.',
                   'Most likely.',
                   'Outlook good.',
                   'Yes.',
                   'Signs point to yes.',
                   'Reply hazy try again.',
                   'Ask again later.',
                   'Better not tell you now.',
                   'Cannot predict now.',
                   'Concentrate and ask again.',
                   'Don\'t count on it.',
                   'My reply is no.',
                   'My sources say no.',
                   'Outlook not so good.',
                   'Very doubtful.']


def dpred(w):  # Returns True if w is an auxiliary verb.
    return w in ['do', 'can', 'should', 'would', 'have', 'could', 'will', 'shall']


randomwords = ['gunsmith', 'membership', 'window',
               'indication', 'ride', 'burgers', 'potatoes']
random_responses = ['Why so random?',
                    'Why did you come up with that?',
                    'You are very creative.',
                    'Let\'s talk about something else.',
                    'Can we talk about something else?',
                    'That triggers me.']
random_response_count = 0


def random_response():
    global random_response_count
    random_response_count += 1
    return random_responses[random_response_count % len(random_responses)]
