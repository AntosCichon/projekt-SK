import pathlib
import os
import shutil
from sys import exit
import numpy
import matplotlib.pyplot as plt

# generates and writes to file {taskcount} tasks
# {timeranges} = [minimal arrival time, maximal arrival time, minimal burst time, maximal burst time]
# returns list of paths to test directories
def generateTestInput(taskcount, timeranges, seed=None):

    numpy.random.seed(seed) # set seed for process generation. if nothing was parsed, use NumPy default
    activedir = pathlib.Path(__file__).parent.resolve() # path to current directory
    pathsToTests = [] # list of paths to created directories
    genfunctions = {
        "randomized" : random,
        "in normal distribution" : binomial,
        "in exponential distribution" : exponential,
        "in ascending order" : ascending,
        "in descending order" : descending
    }

    deleteExistingTests(activedir) # delete all previous test directories

    for i, (arrivaldescription, arrivalgenerator) in enumerate(genfunctions.items()):
        for j, (burstdescription, burstgenerator) in enumerate(genfunctions.items()):
            testnum = i*len(genfunctions)+j # keep track of current test count
            functions = [arrivalgenerator, burstgenerator] # match generator functions for arrival and burst times
            testdirpath = makeTestDir(activedir, testnum+1) # path to test directory
            pathsToTests.append(testdirpath)
            generatedInput = callGenerators(functions, taskcount, timeranges) # call generator function from {genfunctions} array
            generatedInput.insert(0, f'Arrival times {arrivaldescription},\nBurst times {burstdescription}') # first 2 lines are type of generation algorithms used
            drawHistogram(generatedInput, testdirpath, taskcount) 
            fileinput = [f'{line}\n' for line in generatedInput]

            try: # write generated input to file
                file = open(f'{testdirpath}/input.txt', "w")
                file.writelines(fileinput)
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
    # considering test directories are numbered is ascending order starting from 1,
    # delete all directories named <test[number]> untill an error occurs,
    # thus all previous test diretories were deleted

    i = 0
    while True: # infinite loop. breaks on first unsuccesfull attempt of directory deletion

        i += 1
        targetpath = os.path.join(path, f'test{i}') # target directory to delete specified by {i}

        try:
            shutil.rmtree(targetpath) # delete diretory recursively

        except OSError: # /test[i] doesn't exist -> all directories were deleted. Break loop
            print(f'Successfully deleted all previous diretories')
            break
    return

# data generation functions

def random(count, range):
    return numpy.random.randint(range[0], range[1], count)

def binomial(count, range):
    return numpy.random.binomial(range[1], .5, count)

def exponential(count, timerange):
    maxtime = timerange[1]
    propabilites = [.25] # propability of 1st element is 25%
    sumofpropabilities = .25 # keep track of sum of propabilities
    for i in range(1, maxtime-1): # asign each process time propability of previous process decreased by 1/4
        propability = propabilites[i-1]*.75 # calculate current propability
        sumofpropabilities += propability # sum assigned propability
        propabilites.append(propability) # append calculated propability to list
    lastpropability = 1 - sumofpropabilities # all propabilities must add up to 1. This finds missing propability 
    propabilites.append(lastpropability) # assign last propability to last page
    return [num for num in numpy.random.choice(numpy.arange(maxtime)+1, count, p=propabilites)]

def ascending(count, ignore):
    return [i for i in range(count+1)]

def descending(count, ignore):
    return [i for i in range(count-1, -1, -1)]

def callGenerators(functions, count, ranges):
    arrivals = functions[0](count, ranges["arrival"]) # call function for arrival times generation
    bursts = functions[1](count, ranges["burst"]) # call function for burst time generation
    return [f'{i};{arrivals[i]};{bursts[i]}' for i in range(count)]

# draws histogram and saves it in according test directory
def drawHistogram(data, path, maxtask):
    fig, axs = plt.subplots(1, 1) # create plot
    maxArrivaltime = max([int(data[i+1].split(";")[1]) for i in range(maxtask)])
    maxBursttime = max([int(data[i+1].split(";")[2]) for i in range(maxtask)])
    maxYvalue = max(maxArrivaltime, maxBursttime) # find maximal y value of graph
    xrange = [int(data[i+1].split(';')[0]) for i in range(maxtask)] # x points to lay bars on
    yrange = [y for y in range(0, maxYvalue, maxYvalue//10)] # create range from 0 to max y value with roughly 10 steps
    arrheights = [int(data[i+1].split(';')[1]) for i in range(maxtask)] # get arrival times
    burstheights = [int(data[i+1].split(';')[2]) for i in range(maxtask)] # get burst times
    axs.bar(xrange, arrheights, label="Arrival", alpha=1, color='r') # draw arrival times on plot
    axs.bar(xrange, burstheights, label="Burst", alpha=.5, color='b') # draw burst times on plot
    axs.set(title=data[0], xlabel="Process id", yticks=yrange, ylabel="Time")
    axs.legend(loc='upper right')

    plt.savefig(os.path.join(path, 'inputvisual.png')) # save file
    plt.close()
