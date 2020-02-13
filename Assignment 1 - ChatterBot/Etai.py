# Shrink3.py
# A conversational "doctor" simulation modelled loosely
# after J. Weizenbaum's ELIZA.
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version of the program runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

from re import *   # Loads the regular expression module.
import random



moneyTalk = False
def respond(the_input):
    wordlist = split(' ', remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()
    if wordlist[0]=='':
        return "Please type something. Here's an idea:" +\
               PHRASES[random.randint(0,4)]
    if wordlist[0:4] == ['i', 'am', 'a', 'republican']:
        return "You should be ashamed of yourself."
    if wordlist[0:4] == ['i','am', 'a', 'democrat']:
        return "Good choice! Have you always been a democract?"
    if wordlist[0:3] == ['i','like','politics']:
        return "Are you a democract or a republican?"
    if wordlist[0:5] == ['politics', 'do', 'not', 'interest', 'me']:
        return "Just because you do not take an interest in politics" \
               "does not mean that politics will not take an interest in you."
    if 'accident' in wordlist:
        return "There is no such thing as an accident in politics."
    if verbp(wordlist[0]):
        return "What good would it do if I did " +\
              stringify(mapped_wordlist) + '?'
    if wordlist[0:3] == ['do','you','think']:
        return "It is not my job to think for you."
    if wordlist[0:3] == ['i', 'am', 'bored']:
        return phrase()
    if wordlist[0:2] == ['can','you'] or wordlist[0:2]==['could','you']:
        return "Chances are that I " + wordlist[0] + ' ' +\
             stringify(mapped_wordlist[2:]) + ', but will not.'
    if wordlist[0:6] == ['what', 'is', 'your', 'party', 'affiliation', '?']:
        return party()
    if 'money' in wordlist:
        global moneyTalk
        moneyTalk = True
        return "Remember to follow the money."
    if 'four' in wordlist or 'seven' in wordlist:
        return "Four score and seven years ago..."
    if 'no' in wordlist or 'yes' in wordlist:
        return "Have you tried rethinking that?"
    if 'maybe' in wordlist:
        return "I require a more definitive answer."
    if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        return stringify(mapped_wordlist) + '.'
    if wordlist[-1] == '?':
        if moneyTalk: return "Could it be because of money?"
        return "That's a good question."
    return phrase()

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)
PARTY_AFFILIATIONS = ['Democrat, Republican, Communist, Tea']

val = 0
def party():
    global val
    val += 1
    return PARTY_AFFILIATIONS[val % 4]

PHRASES = ['Let us make America great again!',
         'Speak softly and carry a big stick.',
         'Mistakes were made.',
         'The only thing we have to fear is fear itself.']

phrase_count = 0
def phrase():
    'Returns one from a list of default responses.'
    global phrase_count
    phrase_count += 1
    return PHRASES[phrase_count % 4]

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

def introduce():
    return "My name is Penny, and I am a political junkie. " \
           "I was programmed by Etai Liokumovich. If you don't like" \
           "my politics, contact him @ etailkmv@uw.edu." \
           "How can I be of service today?"

def agentName():
    return "Politician"


