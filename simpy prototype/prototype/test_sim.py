import simpy  # For Simulation

# Insert Read File Function Here and pass into the variable
# Sample File
# In MemoryList.txt store here
CAPACITY = 3  # first line
SIZE = [10, 20, 30]  # list of memory

# In JobList.txt store here
PROCESSING_TIME = [1, 3, 4, 6, 4, 2, 3]
ARRIVAL_TIME = [0, 3, 4, 6, 6, 7, 8]
JOB_SIZE = [10, 10, 10, 30, 20, 20, 10]


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
    for i in range(7):

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
        input()


def run_job(env, resources_memory, job):
    # get resources that is match
    process_job = yield resources_memory.get(lambda process_job: process_job == job.job_size)
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


