from scheduler import Scheduler
from algorithm import Algorithm
import sys
from operator import attrgetter

class FixedPriorityAlgorithm(Algorithm):
    def __init__(self):
        pass

    def getNextJob(self, scheduler: Scheduler) -> tuple:
        if not scheduler.readyJobs:
            print("Lista de jobs disponíveis está vazia!", file = sys.stderr)
            return None,None,None
        jobToBeExecuted = max(scheduler.readyJobs, key = attrgetter("priority"))
        jobEndTime = jobToBeExecuted.executionTime - jobToBeExecuted.executedTime + scheduler.time
        jobDeadlineNotMet = jobToBeExecuted.getAbsoluteDeadline() < jobEndTime
        return (jobToBeExecuted, jobEndTime, jobDeadlineNotMet) #retorna o job a ser executado e o provável tempo de término do job. É tarefa do escalonador colocar na lista de eventos o evento de término (se aplicável) e o próximo evento de chegada.

        
