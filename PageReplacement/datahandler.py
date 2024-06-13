import os
import matplotlib.pyplot as plt

# reads input.txt file from given directory
# strips all the numbers and returns list 
def importData(path):

    pathtofile = os.path.join(path, "input.txt") # append filename to test directory path
    inputfile = open(pathtofile, 'r')
    data = inputfile.readlines() # make list of all lines in file
    inputfile.close()
    
    for page in range(1, len(data)): # iterate through lines and remove all whitespaces
        data[page] = data[page].strip()

    return data

# writes a result file in given test directory named {algname}-result.csv format: {available frames};{page faults}
def exportData(path, algname, result):

    pathtofile = os.path.join(path, f'{algname.replace(" ", "")}-result.csv') # append filename to test directory path
    resultfile = open(pathtofile, "w") # make a file named {algname}-result.csv
    resultfile.writelines("frames;faults") # write first line according to .csv file formating convention

    for line in result: # iterate through of data
        resultfile.writelines(f'\n{line[0]};{line[1]}') # write row and insert ; between columns
    resultfile.close()
    return

# create graph of results and save it in test directory
def visualizeData(path, data):
    colors = ['turquoise', 'plum', 'lightcoral', 'khaki'] # colors of different algorithms
    names = list(data.keys()) # get names of results
    frames = [frame for frame in range(data[names[0]][0][0], data[names[0]][-1][0]+1)] # get frame range

    with open(os.path.join(path, 'input.txt'), 'r') as inputfile: # first line of each input.txt file is distribution type
        disttype = inputfile.readline()
    inputfile.close()

    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True) # prepare plot
    for i, alg in enumerate(names): # iterate through each algorithm
        offset = [-.3, -.1, .1, .3] # set offset of each data bar, so they don't overlap
        xrange = [frame+offset[i] for frame in frames] # list of x-axis points to lay bars on based on offset
        faults = [fault[1] for fault in data[alg]] # make a list of faults for each algorithm
        axs.bar(xrange, faults, width=0.2, color=colors[i], label=alg) # create graph
    axs.legend(loc='upper right', title="Algorithm")
    axs.set(title=f'Performance of page swapping algorithms -\n{disttype}', xlabel="Available frames", ylabel="Page faults")
    plt.savefig(os.path.join(path, 'resultgraph.png'))
    plt.close()

