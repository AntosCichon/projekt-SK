from time import time
starttime = time()
from sys import exit
from inputgen import generateTestInput
from firstcomefirstserve import fcfs



def main():

    taskcount = 100 # number of processes to generate
    timeranges = {
        "arrival" : [0, 150],
        "burst" : [0, 150],
    }

    pathsToTest = generateTestInput(taskcount, timeranges)
    return

main()
runtime = time() - starttime
exit(f'Done ({round(runtime, 2)} seconds)')