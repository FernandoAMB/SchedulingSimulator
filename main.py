from scheduler import Scheduler
from job import Job
import edfAlgorithm
import fixedPriorityAlgorithm
import plotly.offline as py
import plotly.figure_factory as ff



def main():
    with open('config.txt') as f:
        lines = f.readlines() #Lê as linhas do arquivo config.txt

    if lines[0].strip("\r\n") == "edf": #Verifica se a primeira linha é "edf", caso não seja, define o algoritmo como sendo o de prioridade fixa
        sched = Scheduler(algorithm = edfAlgorithm.EdfAlgorithm())
    else:
        sched = Scheduler(algorithm = fixedPriorityAlgorithm.FixedPriorityAlgorithm())

    for i in range(1,len(lines)-1): #Lê as informações dos jobs linha a linha, adicionando-os ao scheduler 
        jobProps = [int(prop) if prop.isdigit() else prop for prop in lines[i].split(",")]
        job = Job(executionTime = jobProps[0], deadline = jobProps[1], period = jobProps[2], pid = jobProps[3], priority = jobProps[4])
        sched.addJob(job, 0)

    if int(lines[len(lines)-1]) == 0: #Verifica a última linha, que define até que tempo o algoritmo vai rodar. Caso 0, calcula este tempo para que todos os jobs sejam executados
        endTime = 0
        for event, time in sched.eventsQueue.queue:
            if time + event.job.deadline > endTime:
                endTime = time + event.job.deadline
    else:
        endTime = int((lines[len(lines)-1]))

    sched.readyScheduler()

    while sched.time < endTime:
        sched.runTime()

    print(sched.graph_dict)

    figure = ff.create_gantt(sched.graph_dict, group_tasks = True,colors = sched.colors_dict, index_col="ColorId")
    figure['layout']['xaxis']['type'] = None

    py.plot(figure, filename="gantt_graph.html")



    print("Successful run!")

if __name__ == "__main__":
    main()