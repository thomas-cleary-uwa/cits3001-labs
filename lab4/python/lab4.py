""" CITS3001 Lab 4

Thomas Cleary 21704985
"""

import lab4tests

from collections import deque


def find_path(dictionary, start_word, end_word):
    '''
    returns a list of the word in the shortest path
    from start_word to end_word,
    where successive words are different in only one letter.

    types: dictionary (list), start/end_word (str)
    '''
    dictionary_set = set(dictionary)

    node_neighbours = {key : [] for key in dictionary_set}
    distances       = {start_word : 0}

    queue = deque() # infinite queue
    queue.append(start_word)

    while len(queue) > 0:
        count = len(queue)
        found_end = False

        for i in range(0, count):
            curr_node = queue.popleft()
            curr_node_dist = distances[curr_node]
            curr_node_neighbours = get_neighbours(curr_node, dictionary_set)

            for neighbour in curr_node_neighbours:
                node_neighbours[curr_node].append(neighbour)

                if neighbour not in distances.keys():  # if we have not already visited this neighbour
                    distances[neighbour] = curr_node_dist + 1

                    if neighbour != end_word:
                        queue.append(neighbour)

                    # found the shortest path
                    else: 
                        found_end = True
                        break
            if found_end:
                break
        if found_end:
            break

    # no path found, return an empty list
    if end_word not in distances.keys():
        return []
    
    path = []
    get_path(start_word, end_word, node_neighbours, distances, path)

    return path

 
def get_path(curr_node, end_node, node_neighbours, distances, solution):
    """ recursively build the path into the solution list """
    solution_dist = distances[end_node] + 1

    solution.append(curr_node)

    if len(solution) == solution_dist:
        if curr_node == end_node:
            return True
        else:
            return False

    for neighbour in node_neighbours[curr_node]:

        if distances[curr_node] + 1 == distances[neighbour]:
            if not get_path(neighbour, end_node, node_neighbours, distances, solution):
                del solution[-1]
            else:
                return True



def get_neighbours(node, dictionary):
    """ return a list of all neighbours of the node """
    neighbours = []

    # for characters a->z
    for ordinance in range(ord("A"), ord("Z") + 1):
        char = chr(ordinance)
        node_chars = list(node)

        for i, node_char in enumerate(node_chars):
            if node_char != char:
                neighbour = [char for char in node_chars] # deep copy
                neighbour[i] = char
                neighbour = "".join(neighbour)

                if neighbour in dictionary:
                    neighbours.append(neighbour)

    return neighbours


def get_dictionary(filename):
    """ return the dictionary of words as a list """
    with open(filename, "r") as dict_file:
        dictionary = []
        for line in dict_file:
            dictionary.append(line.strip())

    return dictionary


def main():
    """ run tests """
    small_dictionary = ['AIM', 'ARM', 'ART', 'RIM', 'RAM', 'RAT', 'ROT', 'RUM', 'RUN', 'BOT', 'JAM', 'JOB', 'JAB', 'LAB', 'LOB', 'LOG', 'SUN']
    large_dictionary = get_dictionary("../Dictionary.txt")


    lab4tests.lab4_test("Basic Test", 1, "AIM", "BOT", 6, small_dictionary)
    lab4tests.lab4_test("Basic Test", 2, "LOG", "JAM", 5, small_dictionary)
    lab4tests.lab4_test("Basic Test", 3, "LOG", "SUN", 9, small_dictionary)

    # test for start and end with no path
    lab4tests.lab4_test("No Solution Test", 1, "AIM", "ZZZ", 0, ["AIM", "ARM", "ART", "ZZZ"])


if __name__ == "__main__":
    main()
