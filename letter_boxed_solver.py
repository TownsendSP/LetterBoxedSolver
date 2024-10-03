# Townsend Southard Pantano - tgsoutha@syr.edu

import argparse
import re

verbosity = False

globSols: list[list[str]] = []
globCloseSols: list[str] = []

class solElement:
    def __init__(self, inWord):
        self.word: str = inWord
        self.numUnique = len(set(self.word))
        self.firstChar = self.word[0]
        self.lastChar = self.word[-1]
        self.uniques = set(self.word)
        self.potentialNext: list[solElement] = []
        self.depth = 0
        self.letterList: str = ""
        self.remaining: str = ""
        self.isSolution = False

    def processChildren(self):
        global globSols
        # if there are no potential next words, return
        selfRemaining = set(self.letterList) - set(list(self.word))
        # for each of the children, update the remaining letters
        print(f"Remaining: {self.remaining} Checking word {self.word}") if verbosity else None
        for child in self.potentialNext:
            tempset = selfRemaining - set(list(child.word))
            # child.remaining = [x for x in self.remaining if x not in child.word]
            child.remaining = list(tempset)
            print(
                f"Checking {self.word} -> {child.word} - Self remaining: {selfRemaining} Child remaining: {child.remaining}") if verbosity else None
            child.depth = self.depth + 1
            if len(child.letterList) == 12:
                if len(child.remaining) == 0:
                    globSols.append([self.word, child.word])
                elif len(child.remaining) <= 2:
                    globCloseSols.append(f"{self.word} -> {child.word}")

    def importInitialData(self, validWordList, letterlist):
        self.letterList = list(list(letterlist[0]))
        self.potentialNext = validWordList
        self.remaining = list(list(letterlist[0]))
        self.remaining = [x for x in self.remaining if x not in self.uniques]
        print(f"Word: {self.word} Self.remaining: {self.remaining}") if verbosity else None
        self.depth = 0
        return self


def processSolutions(thing: list[list[(solElement, solElement)]]):
    print("Processing solutions from returned solutions") if verbosity else None
    # flatten the list of lists of tuples into a list of tuples
    flatList = [item for sublist in thing for item in sublist]
    # print the list of tuples
    [print(f"{x[0]} -> {x[1]}") for x in flatList]


def threeWordSolutions():
    # treat the closeSols as if the two words were one word
    [solElement(word) for word in globCloseSols]


class LetterBoxedSolver:
    def __init__(self, groups, dictionary_path):
        self.groups = groups
        self.dictionary_path = dictionary_path
        self.solElements: list[solElement] = []
        self.solutions: list[solElement] = []

    def filter_words(self):
        # string to limit to only scoped characters
        print(f"Verbosity is {verbosity}")
        regexMustMatch = f"^[{self.groups[1]}{self.groups[2]}{self.groups[3]}{self.groups[4]}]+$"
        # regex that prevents any group from being repeated
        regexMustntMatch = (f"(^.*([{self.groups[1]}][{self.groups[1]}])|"
                            f"([{self.groups[2]}][{self.groups[2]}])|"
                            f"([{self.groups[3]}][{self.groups[3]}])|"
                            f"([{self.groups[4]}][{self.groups[4]}]).*$)")
        print(f"Must match: {regexMustMatch}\nMust not match: {regexMustntMatch}") if verbosity else None

        # open dictionary file
        try:
            with open(self.dictionary_path) as file:
                # read all lines from file
                lines = file.readlines()
                lines = [line.lower().strip() for line in lines]
                print(f"Read {len(lines)} lines from file") if verbosity else None
                # filter out words that don't match the regex
                lines = [line for line in lines if not re.search(regexMustntMatch, line)]
                print(f"Filtered to {len(lines)} lines") if verbosity else None
                lines = [line for line in lines if re.match(regexMustMatch, line)]
                print(f"Filtered to {len(lines)} lines") if verbosity else None
                # filter out words that are too short
                lines = [line for line in lines if len(line) >= 3]
                print(f"Filtered to {len(lines)} lines") if verbosity else None
                lines.sort()
                # return the list of words
                self.solElements = [solElement(word) for word in lines]
                return lines
        except FileNotFoundError:
            print(f"File {self.dictionary_path} not found")
            exit(1)

    def solve(self):
        # sorting by number of unique characters, to bring the more useful words forward
        self.solElements.sort(key=lambda x: x.numUnique)
        self.solElements.reverse()
        hundredMostUnique = self.solElements
        lettersaslist = ''.join(self.groups.values()).split()  # extracted the var to be more perfomant
        self.solutions = [
            x.importInitialData([y for y in hundredMostUnique if y.firstChar == x.lastChar], lettersaslist) for x in
            hundredMostUnique]
        [solution.processChildren() for solution in self.solutions]
        print("Processed children") if verbosity else None
        if len(globSols) == 0:
            # when searching for 2-word solutions, close solutions are combined into a single word and logged. Those combined solutions are used here, as if they were a single word, so the 2-word code can be reused
            print("No 2-word solutions found, searching for 3-word solutions")
            firstChunk = [solElement(word) for word in globCloseSols]
            self.solutions = [
                x.importInitialData([y for y in hundredMostUnique if y.firstChar == x.lastChar], lettersaslist) for x in
                firstChunk]
            [solution.processChildren() for solution in self.solutions]

        [print(f"{x[0]} -> {x[1]}") for x in globSols]

def main():
    # use global verbosity variable
    global verbosity
    # Using ArgParse to set up arguments for Letter Boxed Solver
    # region parser_setup
    parser = argparse.ArgumentParser(description="Letter Boxed Solver (nytimes.com/puzzles/letter-boxed)")
    parser.add_argument('-d', '--dictpath', type=str, default=None, help='Path to dictionary file')
    parser.add_argument('-g', '--groups', type=str, default=None, help='Groups, separated by commas')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='increase output verbosity')

    args = parser.parse_args()

    # Check if the user has provided a dictionary path. If not, request it interactively
    if args.dictpath is None:
        args.dictpath = input("Enter the path to the dictionary file: ")

    # Check if the user has provided the groups. If not, request them interactively
    if args.groups is None:
        args.groups = input("Enter the groups separated by commas: ")

    if args.verbose:
        print("Verbose mode is enabled")
        print(f"Solution length: {args.count}")
        print(f"Number of solutions to provide: {args.listlength}")
        print(f"Dictionary path: {args.dictpath}")
        print(f"Groups: {args.groups}")
        verbosity = True
    # endregion

    # Get the character groups from the user
    # groups = input_groups()
    groups = {n: g for (n, g) in zip([1, 2, 3, 4], args.groups.split(','))}

    # Create a new LetterBoxedSolver object
    solver = LetterBoxedSolver(groups, args.dictpath)
    solver.filter_words()
    solver.solve()


if __name__ == '__main__':
    main()
