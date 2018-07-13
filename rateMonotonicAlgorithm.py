from scheduler import Scheduler
from algorithm import Algorithm

class RateMonotonicAlgorithm(Algorithm):
    def __init__(self):
        pass

    def getNextJob(self, scheduler: Scheduler) -> tuple:
        if not scheduler.readyJobs:
            print("Lista de jobs disponíveis está vazia!")
            return None,None,None
        jobToBeExecuted = scheduler.readyJobs[0]
        for job in scheduler.readyJobs[1:-1]:
            if job.priority > jobToBeExecuted.priority:
                jobToBeExecuted = job
        jobEndTime = jobToBeExecuted.executionTime - jobToBeExecuted.executedTime + scheduler.time
        jobDeadlineNotMet = jobToBeExecuted.getAbsoluteDeadline() < jobEndTime
        return (jobToBeExecuted, jobEndTime, jobDeadlineNotMet) #retorna o job a ser executado e o provável tempo de término do job. É tarefa do escalonador colocar na lista de eventos o evento de término (se aplicável) e o próximo evento de chegada.

        
