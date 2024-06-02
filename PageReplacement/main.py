from time import time
from datahandler import importData, exportData, visualizeData
from firstinfirstout import fifo
from leastfrequentlyused import lfu
from leastrecentlyused import lru
from mostfrequentlyused import mfu
from inputgen import generateTestInput
import sys

def main():

    pagecount = 1000  # number of pages per test
    pagerange = 50   # maximal page id
    minframes = 3    # minimal number of frames to test algorithm on
    maxframes = 15    # maximal number of frames to test algorithm on
    usealgorithms = { # dict of used algorithms
        "First in first out" : fifo,
        "Least frequently used" : lfu,
        "Last recently used" : lru,
        "Most frequently used": mfu}


    # generate test directories with input.txt file and inputvisual.png histogram
    # arg1 - number of pages in each input.txt
    # arg2 - maximal page id
    # arg3 - seed for generation. Remove it from call to use random
    # returns list of paths to test directories
    pathsToTests = generateTestInput(pagecount, pagerange, 0)

    for test in range(len(pathsToTests)): # iterate through generated tests

        try: # try to perform test. If error eccurs, skip to next test
            performTest(pathsToTests[test], usealgorithms, minframes, maxframes)
        except:
            print(f'Couldn\'t perform test {test+1}. Skipping this test')
        else:
            print(f'Results of test {test+1} saved in coresponding directory') # if no exceptions were raised, print success message

    return

# perform test with given data
# arg1 - path to test directory (which must cointain input.txt file with input data)
# arg2 - list of algorithms to test on
# arg3, arg4 - minimal and maximal frames to simulate on
def performTest(testpath, algorithms, minframes, maxframes):
    overallResults = {} # dictionary of algorithms and their performance
    inputdata = importData(testpath) # imports and formats input data from specified path to test directory

    for alg in algorithms.keys(): # perform test on each algorithm from {algorithms} dict
        algresult = [] # list for current algorithm results

        for frames in range(minframes, maxframes+1): # test algorithm with every frame count from {minframes} to {maxframes}
            faults = algorithms[alg](inputdata, frames) # result (faults count) of algorithm based on specified number of available frames
            algresult.append([frames, faults]) # append this result to the rest of this algorithm

        overallResults[alg] = algresult # append this algorithms name result to list
        # when all test for this frame range are finished, export data
        # arg1 - path to test directory
        # arg2 - name of the tested algorithm ({alg} is parsed function, thus it has to be {__name__} variable of tested algorithm)
        # arg3 - list of all results based on available frames
        # writes a .csv file with given results in format {available frames};{page faults}
        exportData(testpath, alg, algresult)

    # create graph to visualize results
    # arg1 - path to test directory
    # arg2 - dictionary of algorithm and their performance in this test
    visualizeData(testpath, overallResults)

if __name__ == "__main__":
    starttime = time()
    main()
    runtime = time() - starttime
    sys.exit(f'Done ({round(runtime, 2)} seconds)')
