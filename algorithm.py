from scheduler import Scheduler
import abc


class Algorithm:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def getNextJob(self, scheduler: Scheduler) -> tuple:
        ''' Implementação de como obter o próximo job a executar muda de acordo com algoritmo.
        Retorno: 3-upla contendo o job a executar, o tempo de término do job caso não haja outros eventos, e se o job ultrapassa o deadline. '''
        return
