import simpy  # FOR SIMULATION
import pandas as pd # TO PROCESS DATA

# READ FILE FUNCTION
# READ INTO DATAFRAME FORMAT
memList = pd.read_csv('MemoryList.txt', skiprows=1, header=None, names=['Size'], delimiter=' ')
jobList = pd.read_csv('Joblist.txt', skiprows=1, header=None, names=['JobNumber', 'ArrivalTime', 'ProcessingTime',
                                                                     'JobSize'], delimiter=' ')

# GET NUMBER OF MEMORY BLOCK
of = open('MemoryList.txt')
CAPACITY = int(of.readline())
of.close()

# LIST OF MEMORY SIZE
SIZE = memList['Size'].tolist()

# JOBS VARIABLES
PROCESSING_TIME = jobList['ProcessingTime'].tolist()
ARRIVAL_TIME = jobList['ArrivalTime'].tolist()
JOB_SIZE = jobList['JobSize'].tolist()

# GET TOTAL NUMBER OF JOBS
of = open('Joblist.txt')
TOTAL_JOBS = int(of.readline())
of.close()


# CLASS DECLARATION
class Jobs:
    # INITIALIZE OBJECTS
    def __init__(self, arrival_time, processing_time, job_size):
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.job_size = job_size


# MAIN PROGRAM
def start_simulation(env, resources_memory):

    # LOOP THROUGH NUMBER OF JOBS
    for i in range(TOTAL_JOBS):

        # INITIALIZE CLASS AND ASSIGN VARIABLES
        job = Jobs(arrival_time=ARRIVAL_TIME[i], processing_time=PROCESSING_TIME[i], job_size=JOB_SIZE[i])

        # CALCULATE WAITING TIME FOR EACH JOB
        if i == 0:
            a_time = job.arrival_time
        else:
            a_time = job.arrival_time - ARRIVAL_TIME[i-1]

        # WAIT FOR NEXT JOB TO ARRIVE
        yield env.timeout(a_time)
        # ----TEST PRINT----
        print('job has arrived at ', env.now, ' with size ', job.job_size, ' processing_time ', job.processing_time)
        # RUN JOB
        env.process(run_job(env, resources_memory, job))
        # PRESS ENTER TO EXECUTE NEXT EVENT
        input()


# ----RUN JOB FUNCTION----
def run_job(env, resources_memory, job):
    # FIND RESOURCES THAT SATISFY THE REQUIREMENTS
    process_job = yield resources_memory.get(lambda process_job: process_job >= job.job_size)
    # ----TEST PRINT----
    print(job.job_size, ' is processing... at time ', env.now)
    # TIME NEEDED TO COMPLETE JOB
    yield env.timeout(job.processing_time)
    # JOB COMPLETE
    yield resources_memory.put(process_job)
    print("process finished.. for ", job.job_size, " at ", env.now)


# START SIM
env = simpy.Environment()

# INITIALIZE RESOURCES
resources_memory = simpy.FilterStore(env, capacity=CAPACITY)
# GIVE VALUE FOR EACH MEMORY BLOCK
resources_memory.items = SIZE

env.process(start_simulation(env, resources_memory))
env.run()



