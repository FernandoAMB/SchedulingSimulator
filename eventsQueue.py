from operator import itemgetter
from job import Job

class EventsQueue:
    def __init__(self):
        self.queue = []
    
    def addEvent(self, event, time:int):
        index = 0
        for eventList, eventTime in self.queue:
            if eventTime > time:
                index = self.queue.index((eventList, eventTime))
        self.queue.insert(index, (event, time))

    def getAllEventsInTime(self, time:int) -> list:
        events = [event for event,eventTime in self.queue and eventTime == time] #lista de todos os eventos num dado tempo
        self.queue = sorted(list(set(self.queue) - set(events)), key = itemgetter(1)) # nova fila não tem os eventos retornados, usar set e reordenar pelo segundo valor da tupla pode valer de algo (?)
        return events

    def getNextEventTime(self):
        return self.queue[0][1]


class Event:
    def __init__(self, job:Job, eventType:str):
        self.eventType = eventType
        self.job = job