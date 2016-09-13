from string import ascii_lowercase

from joker.jokerCommandNode import sortable_score
from joker.jokerCommandTree import find_percent_dif


def score_by_functions(original_cmd, input_cmd, scoring_functions):
    """Goes through scoring based on functions.

    Scores are based off inputted list of functions, each should return a number
    between 0.0 and 1.0. Those are then compiled into one 0.0 to 100.0 score.
    Runtime is based off of how long each function takes and how long strings are,
    base is O(longest function runtime).

    :param original_cmd: The string that acts as a model.
    :param input_cmd: String that is to be compared to the original string.
    :param scoring_functions: Functions that return 0.0 to 1.0 scores each and
            take two parameters (original_string and input_string) that order.
    :return: 0.0 to 100.0 score of how similar the two strings are.
    """
    score = 0.0
    for func in scoring_functions:
        score += func(original_cmd, input_cmd)
    return score / len(scoring_functions) * 100.0


def uniform_letter_score(original_cmd, input_cmd):
    """Score 0.0 to 1.0 based off placement of letters.

    Runtime is O(N).

    :param original_cmd: String that acts as a model.
    :param input_cmd: String that is to be compared to the original string.
    :return: 0.0 to 1.0 score of how similar the letter placement is.
    """
    inorder_score = 0.0
    for i in range(min(len(original_cmd), len(input_cmd))):
        if original_cmd[i] is input_cmd[i]:
            inorder_score += 1.0
    inorder_score /= len(original_cmd)
    return inorder_score


def count_letter_score(original_cmd, input_cmd):
    """Compares the two words' on their letter counts.

    Runtime is O(1)

    :param original_cmd: String that acts as a model.
    :param input_cmd: String that is to be compared to the original string.
    :return: 0.0 to 1.0 score of how similar the letter counts are.
    """
    letter_count_score = 0.0
    for letter in ascii_lowercase:
        count_original = original_cmd.count(letter)
        count_input = input_cmd.count(letter)
        if count_original != 0 and count_input != 0 and \
                count_original is count_input:
            letter_count_score += count_original
    letter_count_score /= len(original_cmd)
    return letter_count_score


def length_score(original_cmd, input_cmd):
    """Compares the two strings' lengths.

    Runtime is O(1)

    :param original_cmd: String that acts as a model.
    :param input_cmd: String that is to be compared to the original string.
    :return: 0.0 to 1.0 score of how similar the lengths are.
    """
    length_o = len(original_cmd)
    length_i = len(input_cmd)
    max_num = max(length_o, length_i)
    min_num = min(length_o, length_i)
    return min_num / max_num


def joker_score(original_cmd, input_cmd):
    """Score from 0.0 to 100.0 of how similar the strings are.

    Similar score is based off three things uniform_score, length_score, and
    letter_count_score. Runtime is O(N).

    :param original_cmd:
    :param input_cmd:
    :return:
    """
    return score_by_functions(original_cmd, input_cmd,
                              (length_score, uniform_letter_score,
                               count_letter_score))


def filter_by_function(input_cmd, list_cmds, func=joker_score):
    dic_of_scoring = {}
    for cmd in list_cmds:
        dic_of_scoring[cmd] = joker_score(cmd.cmd, input_cmd)
    return dic_of_scoring


def filter_and_pick_joker(input_cmd, list_cmd, filter=filter_by_function):
    dic_of_scoring = filter(input_cmd, list_cmd)
    best_cmd = None
    best_score = 0.0
    for cmd in dic_of_scoring.keys():
        if dic_of_scoring.get(cmd) > best_score:
            best_cmd = cmd
            best_score = dic_of_scoring.get(cmd)
    return filter_to_function(best_cmd.cmd)


def filter_by_function_str(input_cmd, list_cmds, func=joker_score):
    dic_of_scoring = {}
    for cmd in list_cmds:
        dic_of_scoring[cmd] = joker_score(cmd, input_cmd)
    return dic_of_scoring


def filter_and_pick_joker_str(input_cmd, list_cmd, filter=filter_by_function_str):
    dic_of_scoring = filter(input_cmd, list_cmd)
    best_cmd = None
    best_score = 0.0
    for cmd in dic_of_scoring.keys():
        if dic_of_scoring.get(cmd) > best_score:
            best_cmd = cmd
            best_score = dic_of_scoring.get(cmd)
    return filter_to_function(best_cmd)


def word_dic_net(input_word, dic, percent_range, look_range):
    input_score = int(sortable_score(input_word))
    net = []
    for i in range(input_score, look_range+input_score):
        temp_word_group = dic.get(i)
        if temp_word_group is not None and find_percent_dif(i, input_score) <= percent_range:
            for word in temp_word_group:
                net.append(word)
    lower_range = input_score - look_range
    if lower_range < 0:
        lower_range = 0
    for i in range(lower_range, input_score):
        temp_word_group = dic.get(i)
        if temp_word_group is not None and find_percent_dif(i, input_score) <= percent_range:
            for word in temp_word_group:
                net.append(word)
    return net


def filter_to_function(str_cmd):
    return str_cmd
