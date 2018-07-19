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
            self.executingJob = None
            return
        if deadlineNotMet:
            self.eventsQueue.addEvent(Event(nextJob, "Deadline Not Met"), nextJob.getAbsoluteDeadline())

        if endTime <= self.eventsQueue.getNextEventTime():
            self.eventsQueue.addEvent(Event(nextJob, "end"), endTime)

        self.readyJobs.remove(nextJob)
        self.executingJob = nextJob

    def readyScheduler(self):
        eventsToTreat = self.eventsQueue.getAllEventsInTime(0)
        self.treatEvents(eventsToTreat)
        self.time = 0
        self.getNextJobToExecute()


    def runTime(self):
        try:
            timeToRun = self.eventsQueue.getNextEventTime() - self.time
            if self.executingJob:
                self.executingJob.runTime(timeToRun)
            self.time += timeToRun
            eventsToTreat = self.eventsQueue.getAllEventsInTime(self.time)
            
        except NoNextEventException as e:
            print(e.message, file = sys.stderr)
            print("Ending execution...")
            return
        print(self.generateReport())
        self.treatEvents(eventsToTreat)
            
        self.getNextJobToExecute()

    def treatEvents(self, eventsToTreat):
        
        for event in eventsToTreat: #updating events queue and lists of ready and suspended jobs
            if event.eventType == "arrival":
                if (event.job.period != 0): #if period is equal to 0, the job is aperiodic
                    self.eventsQueue.addEvent(Event(event.job, "arrival"), time = self.time + event.job.period) #adding next job arrival to event queue
                event.job.getReady(self.time)
                self.readyJobs.append(event.job)
                if self.executingJob and self.executingJob.state != "suspended":
                    self.readyJobs.append(self.executingJob)
                if event.job in self.suspendedJobs:
                    self.suspendedJobs.remove(event.job)


                print("arrival of job " + str(event.job.pid))

            elif event.eventType == "end":
                self.suspendedJobs.append(event.job)
                
                print("end of job " + str(event.job.pid))

            elif event.eventType == "Deadline Not Met":
                print("Deadline not met by job", str(event.job.pid) ,"at time", str(self.time), "!", sep = " ", file=sys.stderr)
                event.job.getReady(self.time) #assuming a job that didn't met its deadline gets thrown away (mostly out of laziness)
            else:
                print("Unknown event. This shouldn't be happening.", file=sys.stderr)

    def generateReport(self):
        report = ""
        report += (str(self.executingJob))
        report += '\n'
        report += "time: " + str(self.time) + '\n'
        return report
