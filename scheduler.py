from eventsQueue import EventsQueue, Event, NoNextEventException
from job import Job
import sys
from algorithm import Algorithm

class Scheduler:
    def __init__(self, algorithm:Algorithm):
        self.readyJobs = []
        self.algorithm = algorithm
        self.time = 0
        self.suspendedJobs = []
        self.eventsQueue = EventsQueue()
        self.executingJob = None
    
    def addJob(self, job:Job, time:int):
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

    def runTime(self):
        try:
            timeToRun = self.eventsQueue.getNextEventTime() - self.time
            self.executingJob.runTime(timeToRun)
            self.time = self.eventsQueue.getNextEventTime()
            eventsToTreat = self.eventsQueue.getAllEventsInTime(self.time)
        except NoNextEventException as e:
            print(e.message, file = sys.stderr)
            print("Ending execution...")
            return
        
        for event in eventsToTreat: #updating events queue and lists of ready and suspended jobs
            if event.eventType == "arrival":
                if (event.job.period != 0): #if period is equal to 0, the job is aperiodic
                    self.eventsQueue.addEvent(Event(event.job, "arrival"), time = self.time + event.job.period) #adding next job arrival to event queue
                
                event.job.getReady(self.time)
                self.readyJobs.append(self.executingJob)
                self.readyJobs.append(event.job)
                self.suspendedJobs.remove(event.job)
            elif event.eventType == "end":
                self.suspendedJobs.append(event.job)
            elif event.eventType == "Deadline Not Met":
                print("Deadline not met by job", str(event.job.pid) ,"at time", str(self.time), "!", sep = " ", file=sys.stderr)
                event.job.getReady(self.time) #assuming a job that didn't met its deadline gets thrown away (mostly out of laziness)
            else:
                print("Unknown event. This shouldn't be happening.", file=sys.stderr)
            
        self.getNextJobToExecute()
