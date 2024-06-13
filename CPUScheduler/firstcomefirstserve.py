from copy import copy

def fcfs(original_processes):
    processes = copy(original_processes) # make copy of process list
    time = 0 # set inital simulation time to 0
    for process in processes: # iterate through each process
        time = max(time, process.arrivalTime) # if simulation time is less than arrival time of next process, set it to this arrival time
        time += process.burstTime # add burst time of current process to time (execute process)
        process.setTimes(time) # based on current time set turnaround and waiting times of this process

    return [process.exportCSV() for process in sorted(processes, key=lambda x: x.id)]