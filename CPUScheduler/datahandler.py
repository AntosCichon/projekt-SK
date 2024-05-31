from os import path
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def importData(pathtotest):
    with open(path.join(pathtotest, 'input.txt'), 'r') as file:
        line = file.readlines()
    file.close()
    return [process.strip("\n") for process in line[2:]] # starting from 3rd line (first 2 lines are generation type titles), return list of processes

def exportData(name, data, pathtotest):
    pathtofile = path.join(pathtotest, f'{name.replace(" ", "")}-result.csv') # append filename to test directory path
    resultfile = open(pathtofile, "w") # make a file named {algname}-result.csv
    resultfile.writelines("process id;waiting time") # write first line according to .csv file formating convention

    for line in data: # iterate through of data
        resultfile.writelines(f'\n{line}') # write row and insert ; between columns
    resultfile.close()
    return

def visualizeData(pathstotest, algs):
    
    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True) # prepare plot
    tests = [f'{num+1}' for num in range(len(pathstotest))] # test numbers
    results = {} # initialize results dictionary {"algorithm name" : [results]}

    for algname in algs.keys():
        results[algname] = [] # make dictionary keys

    for i, testpath in enumerate(pathstotest): # enumerate each test
        for algname in results.keys(): # open result file for each algorithm used and set it as value of this test key
            resultfilepath = path.join(testpath, f'{algname.replace(" ", "")}-result.csv')
            with open(resultfilepath, 'r') as file:
                line = file.readlines()
            result = [int(line[i].split(";")[1]) for i in range(1, len(line))]
            results[algname].append(getAverage(result))
    
    x = np.arange(len(tests)) # x points for bars
    offset = [-.2, .2] # offsets so bars don't overlap
    for i, (algname, avgWaittime) in enumerate(results.items()):
        axs.bar(x+offset[i], avgWaittime, width=.4, label=algname) # set bar for each algorithm
    
    # set graph values
    axs.set_xticks(x, tests)
    axs.set_xlabel("test")
    axs.set_ylabel("waiting time")
    axs.set_title("Average waiting time for different scheduling algorithms")
    axs.legend(loc='upper left')
    
    plt.savefig(path.join(Path(__file__).parent.resolve(), "resultgraph.png"))

    plt.close()


def getAverage(list):
    sum = 0
    for num in list:
        sum += num
    return sum/len(list)