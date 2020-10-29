import simpy  # For Simulation
import pandas as pd
import numpy as np

# Insert Read File Function Here and pass into the variable
memList = pd.read_csv('MemoryList.txt', skiprows = 1, header = None, names =['Size'], delimiter=' ')  # Read the file in dataframe
jobList = pd.read_csv('Joblist.txt', skiprows = 1, header = None, names =['JobNumber', 'ArrivalTime', 'ProcessingTime', 'JobSize'],  delimiter=' ')


# Sample File
# Output

of = open('MemoryList.txt')
# In MemoryList.txt store here
# Store variable

CAPACITY = int(of.readline())# first line
of.close()

SIZE = memList['Size'].tolist()
print(SIZE)

# In JobList.txt store here
# Store variable
PROCESSING_TIME = jobList['ProcessingTime'].tolist()
ARRIVAL_TIME = jobList['ArrivalTime'].tolist()
JOB_SIZE = jobList['JobSize'].tolist()

of = open('Joblist.txt')
TOTAL_JOBS = int(of.readline())
of.close()

# Class for jobs
class Jobs:
    # initialize objects for class
    def __init__(self, arrival_time, processing_time, job_size):
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.job_size = job_size


# Run Simulation here
def start_simulation(env, resources_memory):
    # Read File here

    for i in range(TOTAL_JOBS):

        # initialize class and put in list
        job = Jobs(arrival_time=ARRIVAL_TIME[i], processing_time=PROCESSING_TIME[i], job_size=JOB_SIZE[i])

        # To calculate the waiting time for next job
        if i == 0:
            a_time = job.arrival_time
        else:
            a_time = job.arrival_time - ARRIVAL_TIME[i-1]

        # wait for next arrival
        yield env.timeout(a_time)
        print('job has arrived at ', env.now, ' with size ', job.job_size, ' processing_time ', job.processing_time)
        # pass to run job to start simulation
        env.process(run_job(env, resources_memory, job))
        # press enter to execute next event
     #   input()


def run_job(env, resources_memory, job):
    # get resources that is match
    process_job = yield resources_memory.get(lambda process_job: process_job >= job.job_size)
    print(job.job_size, ' is processing... at time ', env.now)
    # time needed to complete job
    yield env.timeout(job.processing_time)
    # job completed
    yield resources_memory.put(process_job)
    print("process finished.. for ", job.job_size, " at ", env.now)

# Start simulation
env = simpy.Environment()

# Resources for the simulation
resources_memory = simpy.FilterStore(env, capacity=CAPACITY)
# give value for each memory block available
resources_memory.items = SIZE

env.process(start_simulation(env, resources_memory))
env.run()

# Read sample text file ?
# pandas -> list
# output file ?

# Gui
# box -> cashier


