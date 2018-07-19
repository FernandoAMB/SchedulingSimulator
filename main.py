from scheduler import Scheduler
from job import Job
import edfAlgorithm
import fixedPriorityAlgorithm




def main():
    job1 = Job(executionTime = 2, deadline = 10, period = 10, pid = 0)
    job2 = Job(executionTime = 4, deadline = 30, period = 30, pid = 1)

    sched = Scheduler(algorithm = edfAlgorithm.EdfAlgorithm())

    sched.addJob(job1, 0)
    sched.addJob(job2, 0)
    endTime = 0
    for event, time in sched.eventsQueue.queue:
        if time + event.job.deadline > endTime:
            endTime = time + event.job.deadline

    print(endTime)
    counter = 0
    sched.readyScheduler()
    while sched.time < endTime and counter < 10:
        print(sched.executingJob, end = '\t')
        print("Time: " + str(sched.time))
        sched.runTime()
        counter += 1


    print("Successful run!")

if __name__ == "__main__":
    main()