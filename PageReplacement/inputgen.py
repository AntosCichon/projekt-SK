import pathlib
import os
import shutil
from sys import exit
import numpy
import matplotlib.pyplot as plt

# tests: 1 - ascending order

# deletes all previous test directories recursively
# then creates new test directories
# then puts input.txt file with {linescount} lines of generated page ids ranging from 1 to {pagerange}
# returns list of paths to created directories
def generateTestInput(linescount, pagerange, seed=None):

    numpy.random.seed(seed) # set seed for page id generation. if nothing was parsed, use NumPy default
    activedir = pathlib.Path(__file__).parent.resolve() # path to current directory
    pathsToTests = [] # list of paths to created directories
    genfunctions = [ascending, uniform, binomial, exponential]

    deleteExistingTests(activedir) # delete all previous test directories

    for testnum in range(len(genfunctions)):

        testdirpath = makeTestDir(activedir, testnum+1) # path to test directory
        pathsToTests.append(testdirpath)
        generatedInput = genfunctions[testnum](linescount, pagerange) # call generator function from {genfunctions} array
        drawHistogram(generatedInput, testdirpath, pagerange) # represent generated data as histogram and save it in test directory
        fileinput = [f'{num}\n' for num in generatedInput] # format generated array of numbers

        try:
            file = open(f'{testdirpath}/input.txt', "w") # create input.txt file
            file.writelines(fileinput) # write generated numbers to input.txt file 
            file.close()
        except:
            exit(f'\nCouldn\'t create input.txt file at {testdirpath}. Forced to exit')
        else: # if no exceptions were raised, print success message
            print("and file input.txt")

    return pathsToTests

# creates directory for specified test and returns its path
def makeTestDir(path, testnum):
    targetpath = os.path.join(path, f'test{testnum}') # target directory to create, specified by {testnum} parameter

    try:
        os.mkdir(targetpath)
    except:
        # should never happen as this directory either didn't exist or was deleted by deleteexistingtest() function
        # if at any point this gets executed, holy moly not good
        exit(f'Couldn\'t create test{testnum} directory at {targetpath}. Forced to exit')
    print(f'Successfully created directory test{testnum} ', end="")
    return targetpath

# deletes all previous test directories and their contents
def deleteExistingTests(path):
    # considering test directories are numbered is ascending order starting on 1,
    # delete all directories named <test[number]> untill an error occurs,
    # thus all previos test diretories were deleted

    i = 0
    while True: # infinite loop. breaks on first unsuccesfull attempt at deleting diretory

        i += 1
        targetpath = os.path.join(path, f'test{i}') # target directory to delete specified by {i}

        try:
            shutil.rmtree(targetpath) # delete diretory recursively

        except OSError: # /test[i] doesn't exist -> all directories were deleted. Break loop
            print(f'Successfully deleted all previous diretories')
            break
    return


# draws histogram and saves it in according test directory
def drawHistogram(data, path, maxpage):
    fig, axs = plt.subplots(1, 1) # create plot
    xrange = [x for x in range(1, maxpage+1)] # x points to lay bars on
    heights = [data.count(page) for page in xrange] # get height of each bar (count of occurences in input file)
    axs.bar(xrange, heights) # representa data on plot (skipped first line of input wchich is type of distribution data was generated by)
    axs.set(title=data[0], xlabel="Page reference", ylabel="Occurrences")

    plt.savefig(os.path.join(path, 'inputvisual.png')) # save file
    plt.close()


# all generator functions

def ascending(lines, pagerange):
    generated = [num % pagerange + 1 for num in range(lines)]
    generated.insert(0, "Pages in ascending order")
    return generated

def uniform(lines, pagerange):
    generated = [num for num in numpy.random.randint(1, pagerange+1, lines)]
    generated.insert(0, "Pages in uniform distribution")
    return generated

def binomial(lines, pagerange):
    generated = numpy.random.binomial(pagerange, .5, lines)
    generated = [num+1 for num in generated]
    generated.insert(0, "Pages in binomial distribution")
    return generated

def exponential(lines, pagerange):
    propabilites = [.5] # propability of 1st element is 50%
    sumofpropabilities = .5 # keep track of sum of propabilities
    for i in range(1, pagerange-1): # asign each page propability of previous page decreased by half
        propability = propabilites[i-1]*.5 # calculate current propability
        sumofpropabilities += propability # sum assigned propability
        propabilites.append(propability) # append calculated propability to list
    lastpropability = 1 - sumofpropabilities # all propabilities must add up to 1. This finds missing propability 
    propabilites.append(lastpropability) # assign last propability to last page
    generated = [num for num in numpy.random.choice(numpy.arange(pagerange)+1, lines, p=propabilites)]
    generated.insert(0, "Pages in exponential distribution")
    return generated