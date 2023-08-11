"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    list=[paragraphs[i] for i in range(len(paragraphs)) if select(paragraphs[i])==True]
    if k>=len(list):
        return ''
    else:
        return list[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def about_topic(paragraphs):
        processed_paragraphs=split(lower(remove_punctuation(paragraphs)))
        for key in topic:
            if key in processed_paragraphs:
                return True
        return False
    return about_topic
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    count=0
    if len(typed_words)==0 or len(reference_words)==0:
        return 0.0
    for i in range(len(typed_words)):
        if i<len(reference_words):
            if typed_words[i] == reference_words[i]:
                count+=1
        elif len(typed_words)>len(reference_words):
            break
    return count/len(typed_words)*100

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    numbers_of_char=len(typed)
    numbers_ave=numbers_of_char / 5
    return numbers_ave/(elapsed/60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    possible_word=min(valid_words,key=lambda x: diff_function(x,user_word,limit))
    if diff_function(possible_word,user_word,limit) > limit:
        return user_word
    else:
        return possible_word

    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if start==goal:
        return 0
    if limit<0:
        return 1124132
    elif len(start)==0:
        return len(goal) 
    elif len(goal)==0:
        return len(start)
    elif start[0]!=goal[0]:
        return 1+shifty_shifts(start[1:],goal[1:],limit-1)
    else:
        return shifty_shifts(start[1:],goal[1:],limit)
    # END PROBLEM 6



def pawssible_patches(start, goal, limit):
    "A diff function that computes the edit distance from START to GOAL."
    
    """Base case 1: If either start or goal is empty, and the remaining operations
    # exceed the limit, return a large value (indicating no valid transformation)"""
    if not start or not goal:
        if len(start)+len(goal)<=limit:
            """print("Base case: one of start or goal is empty,and len <= limit")"""
            return len(start)+len(goal)
        else:
            """print("Base case: one of start or goal is empty,and len > limit")"""
            return float('inf')

    "Base case 2: If the first characters match, no edit is needed"
    if start[0]==goal[0]: # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        """print("Characters match, recursion with next characters")"""
        return pawssible_patches(start[1:],goal[1:],limit)
        # END

    "3: If both start and goal are empty, the edit distance is 0"
    if not start and not goal: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        """print("Base case: both start and goal are empty")"""
        return 0
        # END
    if limit < 0:
        return 12232412


    else:
        """print("Characters don't match, consider add, remove, substitute")"""
        add_diff =1+pawssible_patches(start[:],goal[1:],limit-1) # Fill in these lines
        remove_diff = 1+pawssible_patches(start[1:],goal[:],limit-1)
        substitute_diff =1+ pawssible_patches(start[1:],goal[1:],limit-1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add_diff,remove_diff,substitute_diff)

        # END


"""def final_diff(start, goal, limit):
    A diff function. If you implement this function, it will be used."""
###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    count=0
    for i in range(len(typed)):
        if typed[i]==prompt[i]:
            count+=1
        else:
            break
    ratio=count/len(prompt)
    message={}
    message['id']=user_id
    message['progress']=ratio
    send(message)
    return ratio
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    times=[[times_per_player[i][k+1]-times_per_player[i][k] for k in range(len(words))] for i in range(len(times_per_player))]    
    return game(words,times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    result=[]
    for _ in player_indices:
        "use _ as placeholders for loop variables"
        fastest=[]
        result.append(fastest)
    for w in word_indices:
        "word_indices is a range of number from 1 to len((all_words(game)))"
        fastest_player=min(player_indices,key=lambda player:time(game,player,w))
        result[fastest_player].append(word_at(game,w))
    return result
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
