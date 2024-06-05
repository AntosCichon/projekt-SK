from copy import copy

def lcfs(original_processes):
    processes = copy(original_processes)
    queue = [] 
    finished = []
    time = 0

    while queue or processes: # break when queue is empty and there are no more processes to execute
        # put processes which already arrived in queue
        if processes:
            queue.extend(updateQueue(time, processes))
            if not queue: # if queue is empty, set simulation time to arrival of next process and add it to queue
                    time = processes[0].arrivalTime
                    queue.append(processes.pop(0))
                    
        # sort queue from latest to oldest process
        queue.sort(key=lambda x: x.arrivalTime, reverse=True)

        process = queue.pop(0) # pop process from queue and handle it
        time += process.burstTime # update time by burst time of current process ("execute it")
        process.setTimes(time) # set turnaround and waiting time of this process
        finished.append(process) # add this process to finished list

    return [process.exportCSV() for process in sorted(finished, key=lambda x: x.id)]

def updateQueue(time, processes): # returns processes that arrived by now
    arrived = [] # initialize arrived list
    for process in processes: # add processes to list untill process with arrival time greater than current time occurs
        if process.arrivalTime > time: break
        arrived.append(processes.pop(0)) # add process and pop it from process list
    return arrived