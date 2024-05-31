from time import time
starttime = time()
from sys import exit
from inputgen import generateTestInput
from datahandler import importData, exportData, visualizeData
from makeQueue import makeProcessList
from firstcomefirstserve import fcfs
from lastcomefirstserve import lcfs

def main():

    taskcount = 100 # number of processes to generate
    timeranges = {
        "arrival" : [0, 100],
        "burst" : [0, 100],
    }
    usealgorithms = {
        "First come first serve" : fcfs,
        "Last come first serve" : lcfs
    }

    # 3rd argument is seed for process generation. remove from call to use numpy default
    # return list of paths to test directories
    pathsToTest = generateTestInput(taskcount, timeranges, 0)

    # iterate through each path to test
    for testpath in pathsToTest:
        testinput = makeProcessList(importData(testpath)) # list of processes sorted by arrival time
        testresult = performtest(testinput, usealgorithms, testpath) # result of all algorithms on this test
    visualizeData(pathsToTest, usealgorithms)

def performtest(input, algs, testpath):
    testResult = {}
    for name, alg in algs.items(): # perform this test on each algorithm
        algresult = alg(input)
        testResult[name] = algresult # add dictionary entry for this algorithm
        exportData(name, algresult, testpath) # save results to {name}-result.csv file
    return testResult
    


if __name__ == "__main__":
    starttime = time()
    main()
    runtime = time() - starttime
    exit(f'Done ({round(runtime, 2)} seconds)')