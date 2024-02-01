import random
import os
import sys


def tournament_round(files, ranking):
    next_round = []
    while len(files) > 0:
        print("round: " + str(len(ranking) + 1))
        file1 = random.choice(files)
        files.remove(file1)
        file2 = random.choice(files)
        files.remove(file2)

        with open(file1, 'r') as f1:
            text1 = f1.read()
        with open(file2, 'r') as f2:
            text2 = f2.read()

        with open('test.txt', 'w') as f:
            f.write('OPTION 1:\n')
            f.write(text1)
            f.write('\nOPTION 2:\n')
            f.write(text2)

        winner = input('''
               Within a text editor, compare the two files in test.txt.
               Which one is better? (1 or 2): ''')

        while winner != '1' and winner != '2':
            winner = input('''Invalid input. Please try again.
                           \nWhich one is better? (1 or 2): ''')

        if winner == '2':
            file1, file2 = file2, file1
        next_round.append(file1)
        ranking.append(file2)

    os.remove('test.txt')

    return next_round, ranking


def run_blind_test(dir):
    files = [f for f in os.listdir(dir)
             if os.path.isfile(os.path.join(dir, f))]
    files = [os.path.join(dir, f) for f in files]

    print(files)
    print(len(files))

    if len(files) % 2 != 0:
        print("Error: Number of files must be even.")
        exit()

    ranking = []
    while len(files) > 1:
        files, ranking = tournament_round(files, ranking)

    winner = files[0]

    print("prompts ranking:")
    while len(ranking) > 0:
        file = ranking.pop()
        print(str(len(ranking) + 2) + '. ' + file)
    print("1. " + winner)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("Usage: python3 blind_test.py <directory>")
        exit()
    run_blind_test(args[1])
