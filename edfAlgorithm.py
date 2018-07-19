from scheduler import Scheduler
from algorithm import Algorithm
import sys
from operator import methodcaller

class EdfAlgorithm(Algorithm):
    def __init__(self):
        pass

    def getNextJob(self, scheduler: Scheduler) -> tuple:
        if not scheduler.readyJobs:
            print("Lista de jobs disponíveis está vazia!", file = sys.stderr)
            return None,None,None
        jobToBeExecuted = min(scheduler.readyJobs, key = methodcaller("getSlack", scheduler.time))
        jobEndTime = scheduler.time + (jobToBeExecuted.executionTime - jobToBeExecuted.executedTime)
        jobDeadlineNotMet = jobToBeExecuted.getAbsoluteDeadline() < jobEndTime
        return (jobToBeExecuted, jobEndTime, jobDeadlineNotMet) #retorna o job a ser executado e o provável tempo de término do job. É tarefa do escalonador colocar na lista de eventos o evento de término (se aplicável) e o próximo evento de chegada.

        
