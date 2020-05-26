"""Answers the fishy state puzzle found at the URL below.

https://fivethirtyeight.com/features/somethings-fishy-in-the-state-of-the-riddler/

When you run this script, it will build a csv sheet of the magic words.  From there
you can do things like length comparing.

"""

import re
import csv
from words import StateList

DictOfMatches = {}


def CheckForCharacters(WordToCheck, StateToCheck):
    """Check for presence of characters"""
    # print('Checking {0} and {1}'.format(WordToCheck, StateToCheck))
    Search = re.search('[{0}]'.format(StateToCheck), WordToCheck)

    if Search is not None:
        return True

    else:
        DictOfMatches['{0}'.format(WordToCheck)].append(State)
        return False


with open('wordlist.csv', newline='') as csvfilereader:
    wordreader = csv.reader(csvfilereader, delimiter=' ', quotechar='|')

    print('Working Through List of Words...')

    with open('fishwords.csv', 'w', newline='') as csvfilewriter:
        wordwriter = csv.writer(csvfilewriter, delimiter=' ',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for Word in wordreader:
            DictOfMatches['{0}'.format(Word[0])] = []
            for State in StateList:
                CheckForCharacters(Word[0], State.lower())

            if len(DictOfMatches['{0}'.format(Word[0])]) == 1:
                # print(Word[0], ' - ', DictOfMatches['{0}'.format(Word[0])][0])

                wordwriter.writerow(['{0}'.format(Word[0]), ",", '{0}'.format(DictOfMatches['{0}'.format(Word[0])][0])])
