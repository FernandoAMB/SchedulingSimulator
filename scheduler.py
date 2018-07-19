from eventsQueue import EventsQueue, Event, NoNextEventException
import sys

class Scheduler:
    def __init__(self, algorithm):
        self.readyJobs = []
        self.algorithm = algorithm
        self.time = 0
        self.suspendedJobs = []
        self.eventsQueue = EventsQueue()
        self.executingJob = None
    
    def addJob(self, job, time:int):
        self.eventsQueue.addEvent(Event(job, "arrival"), time)

    def getNextJobToExecute(self):
        nextJob, endTime, deadlineNotMet = self.algorithm.getNextJob(self)
        if nextJob == None:
            self.executingJob == None
            return
        if deadlineNotMet:
            self.eventsQueue.addEvent(Event(nextJob, "Deadline Not Met"), nextJob.getAbsoluteDeadline())

        if endTime <= self.eventsQueue.getNextEventTime():
            self.eventsQueue.addEvent(Event(nextJob, "end"), endTime)

        self.readyJobs.remove(nextJob)
        self.executingJob = nextJob

    def readyScheduler(self):
        self.readyJobs = [event.job for event in self.eventsQueue.getAllEventsInTime(0)]
        self.time = 0
        self.executingJob = self.algorithm.getNextJob(self)[0]
        self.eventsQueue.addEvent(Event(self.executingJob, "arrival"), time = self.time + self.executingJob.period) #adding next job arrival to event queue
        try:
            if (self.eventsQueue.getNextEventTime() > self.executingJob.executionTime):
                self.eventsQueue.addEvent(Event(self.executingJob, "end"), self.time + self.executingJob.executionTime)
        except NoNextEventException:
            self.eventsQueue.addEvent(Event(self.executingJob, "end"), self.executingJob.executionTime)


    def runTime(self):
        try:
            timeToRun = self.eventsQueue.getNextEventTime() - self.time
            print(timeToRun)
            if self.executingJob:
                self.executingJob.runTime(timeToRun)
            eventsToTreat = self.eventsQueue.getAllEventsInTime(self.time + timeToRun)
            self.time += timeToRun
        except NoNextEventException as e:
            print(e.message, file = sys.stderr)
            print("Ending execution...")
            return

        
        for event in eventsToTreat: #updating events queue and lists of ready and suspended jobs
            if event.eventType == "arrival":
                if (event.job.period != 0): #if period is equal to 0, the job is aperiodic
                    self.eventsQueue.addEvent(Event(event.job, "arrival"), time = self.time + event.job.period) #adding next job arrival to event queue
                event.job.getReady(self.time)
                if self.executingJob:
                    self.readyJobs.append(self.executingJob)
                self.readyJobs.append(event.job)
                if event.job in self.suspendedJobs:
                    self.suspendedJobs.remove(event.job)
            elif event.eventType == "end":
                self.suspendedJobs.append(event.job)
            elif event.eventType == "Deadline Not Met":
                print("Deadline not met by job", str(event.job.pid) ,"at time", str(self.time), "!", sep = " ", file=sys.stderr)
                event.job.getReady(self.time) #assuming a job that didn't met its deadline gets thrown away (mostly out of laziness)
            else:
                print("Unknown event. This shouldn't be happening.", file=sys.stderr)
            
        self.getNextJobToExecute()
