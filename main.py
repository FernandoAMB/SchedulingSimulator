from scheduler import Scheduler
from job import Job
import edfAlgorithm
import fixedPriorityAlgorithm





def main():
    job1 = Job(executionTime = 2, deadline = 10, period = 10, pid = 0, priority = 1)
    job2 = Job(executionTime = 4, deadline = 30, period = 30, pid = 1, priority = 0)
    job3 = Job(executionTime = 2, deadline = 6, period = 6, pid = 2, priority = 2)

    sched = Scheduler(algorithm = fixedPriorityAlgorithm.FixedPriorityAlgorithm())

    sched.addJob(job1, 0)
    sched.addJob(job2, 0)
    sched.addJob(job3, 0)
    endTime = 0
    for event, time in sched.eventsQueue.queue:
        if time + event.job.deadline > endTime:
            endTime = time + event.job.deadline

    sched.readyScheduler()

    while sched.time < endTime:
        sched.runTime()


    print("Successful run!")

if __name__ == "__main__":
    main()