from os import path
from pathlib import Path
import matplotlib as mpl
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
    
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True, gridspec_kw={'width_ratios': [7, 1], 'wspace':0}) # prepare plot
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
    colors = ['lightcoral', 'mediumpurple', 'turquoise']
    offset = [-.3, 0, .3] # offsets so bars don't overlap
    for i, (algname, avgWaittime) in enumerate(results.items()):
        axs[0].bar(x+offset[i], avgWaittime, width=.3, label=algname, color=colors[i]) # set bar for each algorithm
    
    for i, (algname, times) in enumerate(results.items()):
        bar = axs[1].bar(0+offset[i]*2, getAverage(times), width=.6, label=algname, color=colors[i])
        axs[1].bar_label(bar, padding=(2-i)*20)
    
    # set graph values
    axs[0].set_xticks(x, tests)
    axs[0].set_xlabel("test")
    axs[0].set_ylabel("waiting time")
    axs[0].set_title("Average waiting time for different scheduling algorithms")
    axs[1].set_xticks([],[])
    axs[1].set_xlabel("algorithm")
    axs[1].legend(loc='upper center')

    for item in (axs[0].get_xticklabels()): item.set_fontsize(6)
    plt.savefig(path.join(Path(__file__).parent.resolve(), "resultgraph.png"))

    plt.close()


def getAverage(list):
    sum = 0
    for num in list:
        sum += num
    return sum/len(list)