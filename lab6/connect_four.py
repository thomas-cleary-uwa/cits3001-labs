""" 
An environment to play Connect 4 agains the agent created for Lab 6 of CITS3001

Authors: Thomas Cleary
"""

from board import C4Board


def play():
    pass


def play_again():
    return input("Play again? (y/n): ").lower()


def main():
    playing = True

    games_played = 1

    while playing:
        print("\n" + ("*" * 4) + " NEW GAME " + ("*" * 4))

        play()

        again = play_again()
        while again not in ["y", "n"]:
            again = play_again()

            if again == "n":
                playing = False
            if again == "y":
                games_played += 1



if __name__ == "__main__":
    main()



