class Job:
    def __init__(self, executionTime:int, deadline:int, period:int ,pid:int, priority = 0):
        self.executionTime = executionTime
        self.deadline = deadline
        self.state = "ready"
        self.executedTime = 0
        self.startTime = 0
        self.period = period
        self.pid = pid
        self.priority = priority

    def getSlack(self, currentTime):
        return self.deadline + self.startTime - currentTime

    def getReady(self, currentTime):
        self.startTime = currentTime
        self.executedTime = 0
        self.state = "ready"

    def getAbsoluteDeadline(self):
        return self.deadline + self.startTime

    def runTime(self, timeToRun):
        self.executedTime += timeToRun
        if (self.executedTime == self.executionTime):
            self.state = "suspended"
        
        

