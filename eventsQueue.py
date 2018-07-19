from operator import itemgetter
from job import Job

class Event:
    def __init__(self, job:Job, eventType:str):
        self.eventType = eventType
        self.job = job

    def __str__(self):
        return str(self.job) + "\t" + self.eventType

class EventsQueue:
    def __init__(self):
        self.queue = []
    
    def addEvent(self, event:Event, time:int):
        self.queue.append((event, time))
        self.queue.sort(key = itemgetter(1), reverse = False)

    def getAllEventsInTime(self, time:int) -> list:
        events = []
        for event, EventTime in self.queue:
            if EventTime == time:
                events.append(event)

        for event in events:
            self.queue.remove((event, time))
        return events

    def getNextEventTime(self) -> int:
        if self.queue:
            return self.queue[0][1]
        else:
            raise NoNextEventException("There is no next event!")
            
class NoNextEventException(Exception):
    def __init__(self, message):
        self.message = message

    