class Process:
    def __init__(self, id, arrivalTime, burstTime):
        self.id : int = id
        self.arrivalTime : int  = arrivalTime
        self.burstTime : int = burstTime
        self.turnaroundTime = None
        self.waitTime = None
    
    def __str__(self):
        return f'process id: {self.id}\narrival time: {self.arrivalTime}\nburst time: {self.burstTime}\nturnaround time: {self.turnaroundTime}\nwaiting time: {self.waitTime}'
    
    def setTimes(self, time): # calculate this process turnaround and wating time based on current simulation time and self arrival and burst times
        self.turnaroundTime = time - self.arrivalTime
        self.waitTime = self.turnaroundTime - self.burstTime
    
    def exportCSV(self): # export self values in .csv way
        return f'{self.id};{self.waitTime}'

def makeProcessList(input): # create a list of process objects sorted by arrival time
    processes = []
    for process in input:
        process = process.split(";")
        processes.append(Process(int(process[0]), int(process[1]), int(process[2])))
    return sorted(processes, key=lambda x: x.arrivalTime)