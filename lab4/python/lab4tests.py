""" test cases for lab 4 """

import lab4


def lab4_test(test_name, test_num, start, end, opt_len, dictionary):
    """ from lab automarker """
    print("{} {}\n...".format(test_name, test_num))
    print("Start Word:   {}".format(start))
    print("End Word:     {}".format(end))
    print("Opt Path Len: {}".format(opt_len))
    print("...")

    found_path = lab4.find_path(dictionary, start, end)

    print("Path Found: ", end="")
    if len(found_path) == 0:
        print("No Path Found")
    else:
        for i, node in enumerate(found_path):
            if i < len(found_path) - 1:
                print("{}-->".format(node), end="")
            else:
                print("{}".format(node))
    print("Path length: {}".format(len(found_path)))

    assert len(found_path) == opt_len, "Found path length {}, does not equal optimal {}".format(
        len(found_path), opt_len)

    print("...")
    print("{} {} Passed.\n\n".format(test_name, test_num))
