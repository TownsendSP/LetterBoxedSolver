# LetterBoxedSolver

This program solves the [daily NYTimes Letter Boxed puzzle](https://www.nytimes.com/puzzles/letter-boxed). Due to the nature of the puzzle, and the
potentially geometric growth of the solution space, the code was designed to restrict the solution space as much as
possible. While the code isn't completely elegant and does use some brute-force elements, care was taken to design it
such that the brute-force tasks were as limited as possible in scope. 

Example Usage:
`python ./letter_boxed_solver.py -d /usr/share/dict/words -g abc,def,ghi,jkl`

The program can also be run completely interactively, but the verbose output is only accesible with the command-line
flag `-v`

Note: Not all words in the system dictionary are allowed words on the nytimes letter boxed, so despite found
solutions, none of them might be allowed. Conversely, there are allowed words that aren't present in the system dictionary. 
There should almost always be a 2-word solution, but it may not be found if the needed words aren't in the used dictionary.
