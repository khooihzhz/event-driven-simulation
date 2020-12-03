import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import simpy
import pandas as pd


class MainMenu:
    def __init__(self, root):
        self.root = root
        # default variables
        self.list_memory = []
        self.list_job_size = []
        self.list_arrival_time = []
        self.list_processing_time = []
        self.alloc_scheme = "FIXED"
        self.alloc_mode = "FIRST-FIT"
        self.num_blocks = 10
        self.dynamic_size = 50000
        # for menu
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.option_menu = tk.Menu(self.menubar, tearoff=0)
        self.fixed_submenu = tk.Menu(self.option_menu, tearoff=0)
        self.dynamic_submenu = tk.Menu(self.option_menu, tearoff=0)
        self.method_menu = tk.Menu(self.menubar, tearoff=0)

        # SET MENUS
        self.setupMenu()
        # SET TITLE
        self.title = tk.Label(self.root, text="WELCOME TO EVENT-DRIVEN SIMULATION PROGRAM")
        # USE FRAME TO SPLIT INTO 3 ELEMENTS
        self.group_text_frame = tk.Frame(self.root)

        # ----- TEXT FIELD ------
        self.memoryTile = tk.Label(self.group_text_frame, text="MEMORY LIST:")
        self.jobTile = tk.Label(self.group_text_frame, text="JOB LIST:")
        self.memoryTextPad = tk.Text(self.group_text_frame, width=51, height=25)  # TEXT PAD TO DISPLAY MEMORY LIST
        self.jobTextPad = tk.Text(self.group_text_frame, width=51, height=25)  # TEXT PAD TO DISPLAY JOB LIST

        self.button = tk.Button(text="START", command=self.startSimulation)  # BUTTON TO RUN SIMULATION
        self.position()

    def setupMenu(self):
        self.root.geometry("1280x720")
        self.root.title("EVENT-DRIVEN SIMULATION PROGRAM")
        self.root.config(menu=self.menubar)  # MENU BAR AND SUBMENU BAR
        # ADD FILE MENU
        self.file_menu.add_command(label="Open Memory List File", command=self.open_memory_file)
        self.file_menu.add_command(label="Open Job List File", command=self.open_job_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit Program", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        # ADD SUBMENU TO THE PARTITION SCHEMES
        self.setupSubMenu()
        # ADD MEMORY ALLOCATION METHOD MENU
        self.method_menu.add_radiobutton(label="FIRST-FIT", command=lambda: self.set_mode("FIRST-FIT"))
        self.method_menu.add_radiobutton(label="BEST-FIT", command=lambda: self.set_mode("BEST-FIT"))
        self.method_menu.add_radiobutton(label="WORST-FIT", command=lambda: self.set_mode("WORST-FIT"))
        self.menubar.add_cascade(label="Method", menu=self.method_menu)

    # FUNCTION TO CREATE SUBMENU
    def setupSubMenu(self):
        # ADD CHOICES FOR NUMBER OF BLOCKS (FIXED)
        self.fixed_submenu.add_radiobutton(label="10 Blocks", command=lambda: self.set_scheme("FIXED", 10))
        self.fixed_submenu.add_radiobutton(label="7 Blocks", command=lambda: self.set_scheme("FIXED", 7))
        self.fixed_submenu.add_radiobutton(label="5 Blocks", command=lambda: self.set_scheme("FIXED", 5))
        self.fixed_submenu.add_radiobutton(label="3 Blocks", command=lambda: self.set_scheme("FIXED", 3))
        self.option_menu.add_cascade(label="Fixed Partition", menu=self.fixed_submenu)
        # ADD CHOICES FOR MEMORY SIZE (DYNAMIC)
        self.dynamic_submenu.add_radiobutton(label="50,000 Size",
                                             command=lambda: self.set_scheme("DYNAMIC", 50000))
        self.dynamic_submenu.add_radiobutton(label="40,000 Size",
                                             command=lambda: self.set_scheme("DYNAMIC", 40000))
        self.dynamic_submenu.add_radiobutton(label="30,000 Size",
                                             command=lambda: self.set_scheme("DYNAMIC", 30000))
        self.dynamic_submenu.add_radiobutton(label="20,000 Size",
                                             command=lambda: self.set_scheme("DYNAMIC", 20000))
        self.option_menu.add_cascade(label="Dynamic Partition", menu=self.dynamic_submenu)
        self.menubar.add_cascade(label="Option", menu=self.option_menu)

    # READ CONTENT IN MEMORY LIST FILE
    def open_memory_file(self):
        try:
            self.memoryTextPad.delete("1.0", tk.END)
            read = tk.filedialog.askopenfilename(title="open file", filetypes=(("Text File", "*.txt"),))
            read = pd.read_csv(read, skiprows=1, header=None, names=['Size'], delimiter=' ')
            self.memoryTextPad.insert(END, read)
            self.list_memory = read  # GET LIST OF MEMORY
            self.list_memory = self.list_memory['Size'].tolist()
        except:
            print("Looks Like you did'nt select a file")

    # READ CONTENT IN JOB LIST FILE
    def open_job_file(self):
        try:
            self.jobTextPad.delete("1.0", tk.END)
            read = tk.filedialog.askopenfilename(title="open file", filetypes=(("Text File", "*.txt"),))
            read = pd.read_csv(read, skiprows=1, header=None, names=['JobNumber', 'ArrivalTime', 'ProcessingTime',
                                                                     'JobSize'], delimiter=' ', index_col=0)
            self.jobTextPad.insert(END, read)
            list_job = read
            self.list_processing_time = list_job['ProcessingTime'].tolist()  # GET PROCESSING TIME
            self.list_arrival_time = list_job['ArrivalTime'].tolist()  # GET ARRIVAL TIME
            self.list_job_size = list_job['JobSize'].tolist()  # GET JOB SIZE
        except:
            print("Looks Like you did'nt select a file")

    # SET FIXED PARTITION
    def set_scheme(self, scheme, num):
        self.alloc_scheme = scheme
        if scheme == "FIXED":
            self.num_blocks = num
        else:
            self.dynamic_size = num

    # SET ALLOCATION MODE
    def set_mode(self, mode):
        if mode == "WORST-FIT":
            if self.alloc_scheme == "FIXED" or self.alloc_scheme == "":
                messagebox.showinfo(title="Wrong Mode!",
                                    message="Worst-fit is not available for fixed partition scheme.")
            else:
                self.alloc_mode = mode
        else:
            self.alloc_mode = mode

    # ELEMENT POSITION
    def position(self):
        self.title.grid(row=0, column=1)
        self.memoryTile.grid(row=2, column=0, sticky=W)
        self.jobTile.grid(row=2, column=2, sticky=W)
        self.memoryTextPad.grid(row=3, column=0)
        self.jobTextPad.grid(row=3, column=2)
        self.button.grid(row=2, column=1)
        self.group_text_frame.grid(row=1, column=1, padx=30)
        col_count, row_count = self.root.grid_size()

        for col in range(col_count):
            self.root.grid_columnconfigure(col, minsize=200)

        for row in range(row_count):
            self.root.grid_rowconfigure(row, minsize=100)

    # run simulation
    def startSimulation(self):
        # if memory or job is empty
        if self.list_memory and self.list_job_size:
            # start sim window
            self.root.destroy()  # destroy current window
            self.root = tk.Tk()
            self.root.geometry("1280x720")
            self.root.title("EVENT-DRIVEN SIMULATION PROGRAM")
            env = simpy.Environment()
            sim = SimulationWindow(self.root, env, self.list_memory, self.list_job_size, self.list_arrival_time,
                                   self.list_processing_time, self.alloc_scheme, self.alloc_mode, self.num_blocks,
                                   self.dynamic_size)
            if self.alloc_scheme == "FIXED":
                env.process(sim.start_FP_simulation())
            else:
                env.process(sim.start_DP_simulation())
            env.run()

        else:
            messagebox.showinfo(title="Unable To Run Simulation", message="Please select memory file/job file, "
                                                                          "scheme, and mode.")


class SimulationWindow:
    def __init__(self, root, env, list_memory, list_job_size, list_arrival_time,
                 list_processing_time, alloc_scheme, alloc_mode, num_of_blocks,
                 dynamic_size):

        # variables for Simulation
        self.root = root  # TKINTER ROOT
        self.env = env  # SIMPY ENVIRONMENT
        self.list_memory = list_memory  # LIST OF MEMORY
        self.list_job_size = list_job_size  # LIST OF JOB_SIZE
        self.list_arrival_time = list_arrival_time  # LIST OF ARRIVAL TIME
        self.list_processing_time = list_processing_time  # LIST OF PROCESSING TIME
        self.alloc_scheme = alloc_scheme  # FIXED/ DYNAMIC
        self.alloc_mode = alloc_mode  # BEST-FIT/ FIRST-FIT/ WORST-FIT
        self.num_blocks = num_of_blocks  # WHEN ITS FIXED
        self.dynamic_size = dynamic_size  # WHEN ITS DYNAMIC
        self.total_processing_time = 0
        # Create Canvas to Draw
        self.drawing_space = tk.Canvas(self.root, width=1280, height=720)

        # ----- TEXT IN CANVAS -----
        self.goBackInstruction = self.drawing_space.create_text(100, 30, text="Press ESC to Show Summary /\n Back to "
                                                                              "Main Menu")
        self.title = self.drawing_space.create_text(600, 30, text="MEMORY MANAGEMENT SIMULATION")  # TITLE FOR SCREEN
        self.display_mode = self.drawing_space.create_text(1000, 90, text=f"Mode : {self.alloc_mode}")  # DISPLAY MODE
        self.display_time = self.drawing_space.create_text(120, 500, text="Time : ")  # DISPLAY TIME
        # DISPLAY PROGRESS
        self.display_progress = self.drawing_space.create_text(800, 525, text="\n\nPress SpaceBar to Start")
        # DISPLAY QUEUE STATUS
        self.display_queue_status = self.drawing_space.create_text(500, 500, text="Queue Status : ")
        # DISPLAY TOTAL EXTERNAL FRAGMENTATION
        self.display_total_frag = self.drawing_space.create_text(160, 600, text="Total Fragmentation : ")

        # ----- END TEXT IN CANVAS -----

        # ----- COORDINATES -----

        # MEMORY BLOCK ON SCREEN
        self.memoryRectangleStart_X = 100  # x1
        self.memoryRectangleStart_Y = 100  # y1
        self.memoryRectangleEnd_X = 1100  # x2
        self.memoryRectangleEnd_Y = 200  # y2

        # JOB QUEUE CONTAINER
        self.jobQueueRectangleStart_X = 100  # x1
        self.jobQueueRectangleStart_Y = 350  # y1
        self.jobQueueRectangleEnd_X = 1100  # x2
        self.jobQueueRectangleEnd_Y = 450  # y2

        # BLOCKS STARTING COORDINATES TO COME IN

        self.jobBlockSize = 30  # size of the block
        self.startLocation_X = 1100  # x1
        self.startLocation_Y = 250  # y1
        # no end X because determined by memory address.
        self.endLocation_Y = 350  # y2

        # Remember Last JOB BLOCK location
        # initially start at where rectangle starts.
        self.lastJobBlock = self.jobQueueRectangleStart_X

        # -----END COORDINATES-----

        # ----- INITIALIZE LIST TO STORE ITEMS -----
        self.jobQueue = []  # store actual job size
        self.jobBlocks = []  # store the coordinates for deletion later
        self.listWaitingTime = [] # to store list of jobs waiting time
        self.totalMemorySize = 0  # to store total memory
        self.maxQueueLength = -1
        self.minQueueLength = 1000

        # DRAW RECTANGLE ON SCREEN
        self.createBlock()

        # Store addresses
        self.listMemoryAddress = []
        # Initialize List to store resources
        self.listMemoryResources = []
        # ----- CHECK FIXED PARTITION -----
        if self.alloc_scheme == "FIXED":
            # calculate internal fragmentation
            self.totalInternalFrag = 0
            # IF FIRST-FIT
            if self.alloc_mode == "FIRST-FIT":
                # CREATE RESOURCES
                self.listAvailableMemory = self.list_memory[:self.num_blocks]  # copy list till n
                # DRAW RECTANGLE

            # IF IT IS BEST FIT
            elif self.alloc_mode == "BEST-FIT":
                self.listAvailableMemory = self.list_memory[:self.num_blocks]  # copy list till n
                # sort list
                self.listAvailableMemory.sort()

            # Calculation for partition line
            self.createMemoryResources()
            self.calculatePartition()  # calculate partitions

        # ----- DYNAMIC ALLOCATION SCHEME -----
        else:
            # SHOW REMAINING MEMORY
            self.display_remainingMemory = self.drawing_space.create_text(600, 600, text="Total Remaining memory : ")
            # Start with n memory
            self.listExFrag = []
            self.totalExFrag = 0
            self.lastExFrag = 0
            self.totalMemorySize = self.dynamic_size  # get total memory for calculation
            self.totalRemainingMemory = self.totalMemorySize  # total remaining memory
            self.createDynamicResources()

        # button to go back
        self.backButton = tk.Button(text="Back", command=self.returnToMainMenu)
        self.root.bind('<Escape>', self.returnToMainMenu)

        # for Summary
        self.counter = 0

        # ----- key_press to continue -----
        self.triggerVar = tk.IntVar()
        self.continueButton = tk.Button(text="Run", command=self.pressToContinue)
        self.root.bind('<space>', self.pressToContinue)
        self.position_blocks()

    def returnToMainMenu(self, event=None):
        # IF WE REACH THE LAST JOB WE SHOW SUMMARY
        print(self.counter, len(self.list_job_size))
        if self.counter == len(self.list_job_size):
            if self.alloc_scheme == "FIXED":
                messagebox.showinfo(title="SIMULATION COMPLETE!",
                                    message=f"------------SUMMARY------------\n\n"
                                            f"Total Number of Jobs = {len(self.list_job_size)}\n"
                                            f"Allocation Scheme = {self.alloc_scheme}\n"
                                            f"Algorithm Used = {self.alloc_mode}\n"
                                            f"Total Number of Memory Blocks = {self.num_blocks}\n"
                                            f"Total Number of Job Undone = {len(self.jobQueue)}\n"
                                            f"Total Internal Fragmentation = {self.totalInternalFrag}\n"
                                            f"Average Internal Fragmentation = "
                                            f"{int(self.totalInternalFrag/self.env.now)}\n"       
                                            f"Throughput "
                                            f"= {(self.total_processing_time / self.env.now):.2f}\n"
                                            f"Total Waiting Time = {self.calculateWaitingTime()}\n"
                                            f"Average Waiting Time = "
                                            f"{(self.calculateWaitingTime()/(len(self.list_job_size) - len(self.jobQueue))):.2f}\n"
                                            f"Maximum Waiting Time = {max(self.listWaitingTime)}\n"
                                            f"Minimum Waiting Time = {min(self.listWaitingTime)}\n"
                                            f"Total Queue Length = {self.calculateWaitingTime()}\n"
                                            f"Average Queue Length = {(self.calculateWaitingTime()/self.env.now):.2f}\n"
                                            f"Maximum Queue Length = {self.maxQueueLength}\n"
                                            f"Minimum Queue Length = {self.minQueueLength}\n")
            else:
                messagebox.showinfo(title="SIMULATION COMPLETE!",
                                    message=f"------------SUMMARY------------\n\n"
                                            f"Total Number of Jobs = {len(self.list_job_size)}\n"
                                            f"Allocation Scheme = {self.alloc_scheme}\n"
                                            f"Algorithm Used = {self.alloc_mode}\n"
                                            f"Total Number of Memory Size = {self.dynamic_size}\n"
                                            f"Total Number of Job Undone = {len(self.jobQueue)}\n"
                                            f"Total External Fragmentation = {self.totalExFrag}\n"
                                            f"Average External Fragmentation = "
                                            f"{int(self.totalExFrag/self.env.now)}\n"
                                            f"Throughput "
                                            f"= {(self.total_processing_time / self.env.now):.2f}\n"
                                            f"Total Waiting Time = {self.calculateWaitingTime()}\n"
                                            f"Average Waiting Time = "
                                            f"{(self.calculateWaitingTime()/(len(self.list_job_size) - len(self.jobQueue))):.2f}\n"
                                            f"Maximum Waiting Time = {max(self.listWaitingTime)}\n"
                                            f"Minimum Waiting Time = {min(self.listWaitingTime)}\n"
                                            f"Total Queue Length = {self.calculateWaitingTime()}\n"
                                            f"Average Queue Length = {(self.calculateWaitingTime()/self.env.now):.2f}\n"
                                            f"Maximum Queue Length = {self.maxQueueLength}\n"
                                            f"Minimum Queue Length = {self.minQueueLength}\n")
        self.root.destroy()
        self.root = tk.Tk()
        MainMenu(self.root)

    # Function to DRAW RECTANGLE ON SCREEN
    def position_blocks(self):
        self.drawing_space.pack()
        self.continueButton.pack()
        self.backButton.pack()

    def createBlock(self):
        # LABEL AND CREATE WAITING LIST CONTAINER
        self.drawing_space.create_text(145, 340, text="WAITING QUEUE")
        self.drawing_space.create_rectangle(self.jobQueueRectangleStart_X, self.jobQueueRectangleStart_Y,
                                            self.jobQueueRectangleEnd_X, self.jobQueueRectangleEnd_Y,
                                            fill="white", outline="green")

        # LABEL AND CREATE MEMORY BLOCK
        self.drawing_space.create_text(145, 90, text="MEMORY BLOCK")
        self.drawing_space.create_rectangle(self.memoryRectangleStart_X, self.memoryRectangleStart_Y,
                                            self.memoryRectangleEnd_X, self.memoryRectangleEnd_Y,
                                            outline="blue", fill="white")

    def createMemoryResources(self):
        # calculate sizes
        for i in range(len(self.listAvailableMemory)):
            self.totalMemorySize += self.listAvailableMemory[i]  # FIND TOTAL
            # add to list in form of [ (CHECK STATUS BUSY/FREE), (SIZE OF MEMORY) )
            self.listMemoryResources.append([False, self.listAvailableMemory[i]])

    def createDynamicResources(self):
        job_id = -1  # indication of no job yet
        memoryEnd_X = int((self.totalMemorySize / self.totalMemorySize * 1000) + self.memoryRectangleStart_X)
        # SAVE STATE, MEMORY SIZE, STARTING ADD, END ADD, JOB ID
        self.listMemoryAddress.append([False, self.totalMemorySize, self.memoryRectangleStart_X,
                                       memoryEnd_X, job_id])

    def calculatePartition(self):
        # loop through all memory size
        memoryStart_X = self.memoryRectangleStart_X

        for memory in self.listAvailableMemory:
            memoryEnd_X = int((memory / self.totalMemorySize * 1000) + memoryStart_X)
            self.listMemoryAddress.append([memory, memoryStart_X, memoryEnd_X])
            memoryStart_X = memoryEnd_X
            self.drawing_space.create_line(memoryStart_X, self.memoryRectangleStart_Y,
                                           memoryStart_X, self.memoryRectangleEnd_Y, fill="blue")

    def pressToContinue(self, event=None):
        self.triggerVar.set(1)

    # ----- FIXED PARTITION ------
    # start fixed partition simulation here
    def start_FP_simulation(self, event=None):
        # loop through number of jobs.
        for i in range(len(self.list_job_size)):
            self.counter += 1  # to see if we reached the final job
            # initialize class and assign variables
            job = Jobs(arrival_time=self.list_arrival_time[i],
                       processing_time=self.list_processing_time[i],
                       job_size=self.list_job_size[i], job_id=i + 1)

            self.total_processing_time += job.processingTime
            # calculate total wait time
            if i == 0:
                waitTime = job.arrivalTime
            else:
                waitTime = job.arrivalTime - self.list_arrival_time[i - 1]

            # stop time
            yield self.env.timeout(waitTime)

            # STOP AND WAIT FOR KEY PRESS
            self.continueButton.wait_variable(self.triggerVar)

            # SHOW PROGRESSIONS
            time = f"Time: {self.env.now}"
            self.drawing_space.itemconfigure(self.display_time, text=time)
            progress = f"Event: \nJob {job.jobId} Arrived at Time: " \
                       f"{self.env.now},\nSize: {job.jobSize}, \nProcessing " \
                       f"Time: {job.processingTime}\n"
            self.drawing_space.itemconfigure(self.display_progress, text=progress)

            # check if space for job
            if self.alloc_mode == "FIRST-FIT":
                self.env.process(self.fpFirstFit(job))  # process the job
            else:
                self.env.process(self.fpBestFit(job))  # process job

    # alloc_mode = fixed, first fit
    def fpFirstFit(self, job):
        # loop through to find available blocks
        for index, memoryBlock in enumerate(self.listMemoryResources):
            # check first available memory block
            if memoryBlock[1] >= job.jobSize and memoryBlock[0] is False:
                # check if the job is in queue
                self.checkQueueBlock(job)

                # Get coordinates
                jobStart_X = self.listMemoryAddress[index][1]
                jobEnd_X = int(self.listMemoryAddress[index][1] + (job.jobSize / self.totalMemorySize * 1000))

                # Get Fragmentation Coordinate
                intFragStart_X = jobEnd_X
                intFragEnd_X = self.listMemoryAddress[index][2]  # end of memory block

                # calculate internal fragmentation = memory block size - job size
                intFrag = self.listMemoryAddress[index][0] - job.jobSize
                # ----- TEXT DESCRIPTION -----
                frag = f"Total Internal Fragmentation: {self.totalInternalFrag} + {intFrag}"
                self.drawing_space.itemconfigure(self.display_total_frag, text=frag)

                self.totalInternalFrag += intFrag
                # create block and place in memory block

                processingJob, intFrag = self.createMemoryBlocks(jobStart_X, jobEnd_X,
                                                                 intFragStart_X, intFragEnd_X)

                self.listMemoryResources[index][0] = True  # SET BLOCK AS BUSY

                # WAIT JOB TO BE COMPLETED
                yield self.env.timeout(job.processingTime)  # this is part of simpy library

                # WAIT FOR KEY PRESS  --> EVENT = JOB DONE
                self.continueButton.wait_variable(self.triggerVar)

                # LOOP THROUGH QUEUE TO SEE IF THERE IS SPACE
                for waitingJob in self.jobQueue:
                    self.env.process(self.fpFirstFit(waitingJob))  # put into this function and let it run through

                # release memory
                self.listMemoryResources[index][0] = False

                # ----- SHOW TEXT -----
                finish = f"Job {job.jobId} Finished : At time {self.env.now}"
                self.drawing_space.itemconfigure(self.display_progress, text=finish)
                time = f"Time: {self.env.now}"
                self.drawing_space.itemconfigure(self.display_time, text=time)

                self.removeMemoryBlocks(processingJob, intFrag)  # REMOVE ANIMATION

                return  # exit for loops

        # no slot for job
        if job in self.jobQueue:  # if it is in queue do nothing
            pass
        else:
            self.putQueue(job)  # put job into queue

    # alloc_mode = fixed, best fit
    def fpBestFit(self, job):
        # check if there is a result
        found = False
        # variable to compare
        intFrag = 10e9
        index = 10000

        # check if which block has smallest internal fragmentation
        for memory, memoryBlock in enumerate(self.listMemoryResources):
            # it can fit the job and not occupied
            if memoryBlock[1] >= job.jobSize and memoryBlock[0] is False:
                difference = memoryBlock[1] - job.jobSize

                # if Fragmentation is larger than the difference take this block
                if difference < intFrag:
                    intFrag = difference
                    index = memory
                    found = True  # indicate there is at least one slot to fit

        # if we can find a place to fit the job
        if found is True:
            # check if job is in queue
            self.checkQueueBlock(job)

            # Get coordinates
            jobStart_X = self.listMemoryAddress[index][1]
            jobEnd_X = int(self.listMemoryAddress[index][1] + (job.jobSize / self.totalMemorySize * 1000))

            # Get Fragmentation Coordinate
            intFragStart_X = jobEnd_X
            intFragEnd_X = self.listMemoryAddress[index][2]  # end of memory block

            # calculate internal fragmentation = memory block size - job size
            intFrag = self.listMemoryAddress[index][0] - job.jobSize
            # ----- TEXT DESCRIPTION -----
            frag = f"Total Internal Fragmentation: {self.totalInternalFrag} + {intFrag}"
            self.drawing_space.itemconfigure(self.display_total_frag, text=frag)

            self.totalInternalFrag += intFrag

            # create block and place in memory block

            processingJob, intFrag = self.createMemoryBlocks(jobStart_X, jobEnd_X,
                                                             intFragStart_X, intFragEnd_X)

            self.listMemoryResources[index][0] = True  # SET BLOCK AS BUSY

            # WAIT JOB TO BE COMPLETED
            yield self.env.timeout(job.processingTime)  # this is part of simpy library

            # WAIT FOR KEY PRESS  --> EVENT = JOB DONE
            self.continueButton.wait_variable(self.triggerVar)

            # LOOP THROUGH QUEUE TO SEE IF THERE IS SPACE
            for waitingJob in self.jobQueue:
                self.env.process(self.fpBestFit(waitingJob))  # put into this function and let it run through

            # release memory
            self.listMemoryResources[index][0] = False

            # ----- SHOW TEXT -----
            finish = f"Job {job.jobId} Finished : At time {self.env.now}"
            self.drawing_space.itemconfigure(self.display_progress, text=finish)
            time = f"Time: {self.env.now}"
            self.drawing_space.itemconfigure(self.display_time, text=time)
            frag = f"Total External Fragmentation: {self.totalInternalFrag}"
            self.drawing_space.itemconfigure(self.display_total_frag, text=frag)

            self.removeMemoryBlocks(processingJob, intFrag)  # REMOVE ANIMATION

            return  # exit for loops

        # otherwise there is no place for the job
        else:
            # no slot for job
            if job in self.jobQueue:  # if it is in queue do nothing
                pass
            else:
                self.putQueue(job)  # put job into queue

    # ----- END FIXED PARTITION ------

    # ----- DYNAMIC PARTITIONS  ------
    def start_DP_simulation(self, event=None):
        # loop through number of jobs.
        for i in range(len(self.list_job_size)):
            self.counter += 1
            # initialize class and assign variables
            job = Jobs(arrival_time=self.list_arrival_time[i],
                       processing_time=self.list_processing_time[i],
                       job_size=self.list_job_size[i], job_id=i + 1)
            self.total_processing_time += job.processingTime

            # calculate total wait time
            if i == 0:
                waitTime = job.arrivalTime
            else:
                waitTime = job.arrivalTime - self.list_arrival_time[i - 1]

            # stop time
            yield self.env.timeout(waitTime)

            # STOP AND WAIT FOR KEY PRESS
            self.continueButton.wait_variable(self.triggerVar)

            # ----- TEXT TO SHOW DESCRIPTION----
            time = f"Time: {self.env.now}"
            self.drawing_space.itemconfigure(self.display_time, text=time)
            progress = f"Event: \nJob {job.jobId} Arrived at Time: " \
                       f"{self.env.now},\nSize: {job.jobSize}, \nProcessing " \
                       f"Time: {job.processingTime}\n"
            self.drawing_space.itemconfigure(self.display_progress, text=progress)

            # check which mode to use
            if self.alloc_mode == "FIRST-FIT":
                self.env.process(self.dpFirstFit(job))
            elif self.alloc_mode == "BEST-FIT":
                self.env.process(self.dpBestFit(job))
            else:
                self.env.process(self.dpWorstFit(job))

    def dpFirstFit(self, job):
        # loop through available memory
        for index, memory in enumerate(self.listMemoryAddress):
            if memory[1] >= job.jobSize and memory[0] is False:
                # check if job is in queue
                self.checkQueueBlock(job)

                self.listMemoryAddress[index][0] = True
                self.listMemoryAddress[index][4] = job.jobId  # record job id
                # SPLIT MEMORY BLOCK

                jobStart_X, jobEnd_X, emptySpaceEnd_X, remaining_memory = self.splitMemoryBlock(job, index)

                # insert into list of memory
                self.listMemoryAddress.insert(index + 1, ([False, remaining_memory, jobEnd_X, emptySpaceEnd_X, -1]))

                # ----- EXTERNAL FRAGMENTATION ------
                rem = f"Total Remaining Memory: {self.totalRemainingMemory}"
                self.drawing_space.itemconfigure(self.display_remainingMemory, text=rem)
                # recalculate if there is external Frag
                self.clearExtFrag()
                self.showExtFrag()

                # CREATE BLOCK ANIMATION
                # set internal fragmentation to 0
                processingJob, intFrag = self.createMemoryBlocks(jobStart_X, jobEnd_X, 0, 0)

                # wait job to be finished
                yield self.env.timeout(job.processingTime)
                # wait for key press
                self.continueButton.wait_variable(self.triggerVar)
                self.freeMemoryBlock(job, processingJob)

                # ----- EXTERNAL FRAGMENTATION ------
                rem = f"Total Remaining Memory: {self.totalRemainingMemory}"
                self.drawing_space.itemconfigure(self.display_remainingMemory, text=rem)
                # recalculate if there is external Frag
                self.clearExtFrag()
                self.showExtFrag()

                return  # break loop

        # else if no space for it
        if job in self.jobQueue:
            pass
        else:
            self.putQueue(job)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

    def dpBestFit(self, job):
        found = False
        # find smallest difference
        difference = 10e9
        index = 10000  # use to store index for later use

        for location, memory in enumerate(self.listMemoryAddress):
            # if found job can fit into block and  is not occupied
            if memory[1] >= job.jobSize and memory[0] is False:
                leftOverMemory = memory[1] - job.jobSize
                if leftOverMemory < difference:
                    difference = leftOverMemory
                    index = location
                    found = True

        if found is True:
            # temporarily clear external frag for recalculation
            self.clearExtFrag()
            # check if job ald in job queue
            self.checkQueueBlock(job)

            # set the part as occupied
            self.listMemoryAddress[index][0] = True
            self.listMemoryAddress[index][4] = job.jobId

            # found job split memory block
            jobStart_X, jobEnd_X, emptySpaceEnd_X, remaining_memory = self.splitMemoryBlock(job, index)

            self.listMemoryAddress.insert(index + 1, ([False, remaining_memory, jobEnd_X, emptySpaceEnd_X, -1]))

            # ----- EXTERNAL FRAGMENTATION ------
            rem = f"Total Remaining Memory: {self.totalRemainingMemory}"
            self.drawing_space.itemconfigure(self.display_remainingMemory, text=rem)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

            # create block
            processingJob, intFrag = self.createMemoryBlocks(jobStart_X, jobEnd_X, 0, 0)

            # WAIT job to be finished
            yield self.env.timeout(job.processingTime)

            # job done wait for key press
            self.continueButton.wait_variable(self.triggerVar)
            self.freeMemoryBlock(job, processingJob)

            # ----- EXTERNAL FRAGMENTATION ------
            rem = f"Total Remaining Memory: {self.totalRemainingMemory}"
            self.drawing_space.itemconfigure(self.display_remainingMemory, text=rem)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

            return

        # else if no space for it
        if job in self.jobQueue:
            pass
        else:
            self.putQueue(job)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

    def dpWorstFit(self, job):

        found = False
        # find smallest difference
        difference = -1000
        index = 10000  # use to store index for later use

        for location, memory in enumerate(self.listMemoryAddress):
            # if found job can fit into block and  is not occupied
            if memory[1] >= job.jobSize and memory[0] is False:
                leftOverMemory = memory[1] - job.jobSize
                if leftOverMemory > difference:
                    difference = leftOverMemory
                    index = location
                    found = True

        if found is True:
            # temporarily clear external frag for recalculation
            self.clearExtFrag()
            # check if job ald in job queue
            self.checkQueueBlock(job)

            # set the part as occupied
            self.listMemoryAddress[index][0] = True
            self.listMemoryAddress[index][4] = job.jobId

            # found job split memory block
            jobStart_X, jobEnd_X, emptySpaceEnd_X, remaining_memory = self.splitMemoryBlock(job, index)

            self.listMemoryAddress.insert(index + 1, ([False, remaining_memory, jobEnd_X, emptySpaceEnd_X, -1]))

            # ----- EXTERNAL FRAGMENTATION ------
            rem = f"Total Remaining Memory: {self.totalRemainingMemory}"
            self.drawing_space.itemconfigure(self.display_remainingMemory, text=rem)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

            # create block
            processingJob, intFrag = self.createMemoryBlocks(jobStart_X, jobEnd_X, 0, 0)

            # WAIT job to be finished
            yield self.env.timeout(job.processingTime)
            # job done wait for key press
            self.continueButton.wait_variable(self.triggerVar)
            self.freeMemoryBlock(job, processingJob)

            # ----- EXTERNAL FRAGMENTATION ------
            rem = f"Total Remaining Memory: {self.totalRemainingMemory}"
            self.drawing_space.itemconfigure(self.display_remainingMemory, text=rem)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

            return

        # else if no space for it
        if job in self.jobQueue:
            pass
        else:
            self.putQueue(job)
            # recalculate if there is external Frag
            self.clearExtFrag()
            self.showExtFrag()

    # ----- EXTERNAL FRAGMENTATION FUNCTIONS -----

    # calculate fragmentation
    def showExtFrag(self):
        externalFrag = 0
        if self.jobQueue:
            totalJobSize = 0
            # get total size of jobs in job queue
            for job in self.jobQueue:
                totalJobSize += job.jobSize

            # THIS IS TO CHECK WHETHER THR IS SPACE FOR THE JOB
            for index, memory in enumerate(self.listMemoryAddress):
                for job in self.jobQueue:
                    if memory[1] >= job.jobSize:
                        return      # break out function cuz there is space for job
                    else:
                        pass        # else do nothing

            # if this is the case, show external fragmentation
            if self.totalRemainingMemory >= totalJobSize :
                for index, memory in enumerate(self.listMemoryAddress):
                    if memory[0] is False:
                        exFrag = self.createExFrag(memory[2], memory[3])  # create external fragmentation
                        print(memory[2], memory[3])
                        self.listExFrag.append(exFrag)

                if self.lastExFrag == self.totalRemainingMemory:
                    # ----TEXT DESCRIPTION-----
                    frag = f"Total External Fragmentation: {self.totalExFrag} (increased -> 0)"
                    self.drawing_space.itemconfigure(self.display_total_frag, text=frag)
                else:
                    self.totalExFrag += self.totalRemainingMemory
                    externalFrag = self.totalRemainingMemory
                    self.lastExFrag = externalFrag
                    # ----TEXT DESCRIPTION-----
                    frag = f"Total External Fragmentation: {self.totalExFrag} (increased -> {externalFrag})"
                    self.drawing_space.itemconfigure(self.display_total_frag, text=frag)
            else:
                # ----TEXT DESCRIPTION-----
                frag = f"Total External Fragmentation: {self.totalExFrag} (increased -> 0)"
                self.drawing_space.itemconfigure(self.display_total_frag, text=frag)

    def createExFrag(self, exFragStart, exFragEnd):
        exFrag = self.drawing_space.create_rectangle(exFragStart, self.memoryRectangleStart_Y,
                                                     exFragEnd, self.memoryRectangleEnd_Y, fill="blue")
        return exFrag

    # remove fragmentation
    def clearExtFrag(self):
        for frag in self.listExFrag:
            self.drawing_space.delete(frag)

    def splitMemoryBlock(self, job, index):
        jobStart_X = self.listMemoryAddress[index][2]  # get coordinate of starting block
        # calculate obj length
        jobEnd_X = int(self.listMemoryAddress[index][2] + (job.jobSize / self.totalMemorySize * 1000))

        # split them up
        emptySpaceEnd_X = self.listMemoryAddress[index][3]
        self.listMemoryAddress[index][3] = jobEnd_X
        memorySize = self.listMemoryAddress[index][1]  # get size of block
        remaining_memory = memorySize - job.jobSize  # left over
        self.listMemoryAddress[index][1] = job.jobSize  # change the original memory block to the job size

        self.totalRemainingMemory -= job.jobSize  # for external fragmentation later

        return jobStart_X, jobEnd_X, emptySpaceEnd_X, remaining_memory

    def freeMemoryBlock(self, job, processingJob):

        for index, memory in enumerate(self.listMemoryAddress):
            # find memory block with the job id
            if self.listMemoryAddress[index][4] == job.jobId:
                # release memory
                self.listMemoryAddress[index][0] = False
                self.totalRemainingMemory += self.listMemoryAddress[index][1]  # add back into pool
                self.combineMemoryBlock()  # check if blocks can  be combined

                self.removeMemoryBlocks(processingJob, None)

                for waitingJob in self.jobQueue:
                    if self.alloc_mode == "FIRST-FIT":
                        self.env.process(self.dpFirstFit(waitingJob))
                    elif self.alloc_mode == "BEST-FIT":
                        self.env.process(self.dpBestFit(waitingJob))
                    elif self.alloc_mode == "WORST-FIT":
                        self.env.process(self.dpWorstFit(waitingJob))

        # ---- TEXT FOR PROGRESSION -----
        finish = f"Job {job.jobId} Finished at time [{self.env.now}]"
        self.drawing_space.itemconfigure(self.display_progress, text=finish)
        time = f"Time: {self.env.now}"
        self.drawing_space.itemconfigure(self.display_time, text=time)

    def combineMemoryBlock(self):
        for index, memory in enumerate(self.listMemoryAddress):
            # search for empty spaces
            if index == 0:
                continue  # ignore first slot

            # check if current and previous is empty
            if self.listMemoryAddress[index][0] is False and self.listMemoryAddress[index - 1][0] is False:
                # combine them together
                self.listMemoryAddress[index][1] += self.listMemoryAddress[index - 1][1]
                # swap address
                self.listMemoryAddress[index][2] = self.listMemoryAddress[index - 1][2]
                # pop previous address
                self.listMemoryAddress.pop(index - 1)
                # run for loop again
                self.combineMemoryBlock()
                return  # break current loop

            else:
                # do nothing if no empty spaces
                continue

    # ----- END EXTERNAL FRAGMENTATION FUNCTIONS -----

    # ----- MEMORY BLOCK ANIMATION FUNCTIONS -----

    def createMemoryBlocks(self, jobStart_X, jobEnd_X, intFragStart_X, intFragEnd_X):
        processingJob = self.drawing_space.create_rectangle(self.startLocation_X + jobStart_X,
                                                            self.startLocation_Y,
                                                            self.startLocation_X + jobEnd_X,
                                                            self.endLocation_Y, fill="red")

        if self.alloc_scheme == "FIXED":
            intFrag = self.drawing_space.create_rectangle(self.startLocation_X + intFragStart_X,
                                                          self.startLocation_Y,
                                                          self.startLocation_X + intFragEnd_X,
                                                          self.endLocation_Y, fill="cyan")
        else:
            intFrag = None

        self.moveMemoryBlocks(processingJob=processingJob, intFrag=intFrag, jobStart_X=jobStart_X)
        return processingJob, intFrag

    def moveMemoryBlocks(self, processingJob, intFrag, jobStart_X):
        # get coordinates
        x1, y1, x2, y2 = self.drawing_space.coords(processingJob)

        # check if it reached endpoint

        if x1 == jobStart_X:
            # check if it reach max height
            if y1 == self.memoryRectangleStart_Y:
                return  # exit
            else:
                # move up
                self.drawing_space.move(processingJob, 0, -2)

                # if it is fixed partition there will be intFrag, move it too
                if self.alloc_scheme == "FIXED":
                    self.drawing_space.move(intFrag, 0, -2)

                # keep doing the function until condition is met
                self.drawing_space.after(1, lambda: self.moveMemoryBlocks(processingJob, intFrag, jobStart_X))

        else:
            # move left
            self.drawing_space.move(processingJob, -2, 0)

            # if it is fixed partition there will be intFrag, move it too
            if self.alloc_scheme == "FIXED":
                self.drawing_space.move(intFrag, -2, 0)

            # keep doing the function until condition is met
            self.drawing_space.after(1, lambda: self.moveMemoryBlocks(processingJob, intFrag, jobStart_X))

    def removeMemoryBlocks(self, processingJob, intFrag):
        # get coordinates
        x1, y1, x2, y2 = self.drawing_space.coords(processingJob)
        # check if x1 is out of map
        if y1 == -100:
            return
        else:
            # keep move up
            self.drawing_space.move(processingJob, 0, -1)
            if self.alloc_scheme == "FIXED":
                self.drawing_space.move(intFrag, 0, -1)
            self.drawing_space.after(1, lambda: self.removeMemoryBlocks(processingJob, intFrag))
    # ----- END MEMORY BLOCK ANIMATION FUNCTIONS -----

    # ----- JOB BLOCK IN QUEUE ANIMATION FUNCTIONS -----
    def putQueue(self, job):
        if len(self.jobQueue) < self.minQueueLength:
            self.minQueueLength = len(self.jobQueue)
        status = f"Queue Status : {job.jobId} is in the waiting queue at time {self.env.now}"
        self.drawing_space.itemconfigure(self.display_queue_status, text=status)
        self.jobQueue.append(job)  # add into queue
        # CHECK FOR MAX AND MIN QUEUE LENGTH
        if len(self.jobQueue) > self.maxQueueLength:
            self.maxQueueLength = len(self.jobQueue)

        self.createQueueBlock()

    def createQueueBlock(self):
        # ALL ELEMENTS IN QUEUE HAVE SAME SIZE
        # LOGIC = get last job block coordinates and create another one behind it.
        queueBlock = self.drawing_space.create_rectangle(self.lastJobBlock, self.jobQueueRectangleStart_Y,
                                                         self.lastJobBlock + self.jobBlockSize,
                                                         self.jobQueueRectangleEnd_Y, fill="red", outline="green")

        self.jobBlocks.append(queueBlock)
        self.lastJobBlock += self.jobBlockSize  # increase last block coordination

    def removeFromQueue(self, job):
        # get index of job block
        index = self.jobQueue.index(job)
        # CALCULATE WAITING TIME
        waitingTime = self.env.now - job.arrivalTime
        self.listWaitingTime.append(waitingTime)
        # END
        # START DELETE ANIMATION
        self.removeQueueBlocks(self.jobBlocks[-1])
        self.lastJobBlock -= self.jobBlockSize
        self.jobBlocks.remove(self.jobBlocks[-1])
        self.jobQueue.pop(index)

        # ----- text description
        status = f"Queue Status : Job {job.jobId} left queue at time [{self.env.now}]"
        self.drawing_space.itemconfigure(self.display_queue_status, text=status)

    def removeQueueBlocks(self, queueBlock):
        x1, y1, x2, y2 = self.drawing_space.coords(queueBlock)
        # start animation
        if y1 == -100:
            return  # use to break out function
        else:
            # keep move down
            self.drawing_space.move(queueBlock, 0, 2)
            self.drawing_space.after(1, lambda: self.removeQueueBlocks(queueBlock))

    # to check if job is in queue
    def checkQueueBlock(self, job):
        if job in self.jobQueue:
            self.continueButton.wait_variable(self.triggerVar)
            self.removeFromQueue(job)

    def calculateWaitingTime(self):
        totalWaitingTime = 0
        for t in self.listWaitingTime:
            totalWaitingTime += t

        return totalWaitingTime

    # ----- END JOB IN QUEUE ANIMATION FUNCTIONS -----


class Jobs:
    # INITIALIZE OBJECTS
    def __init__(self, arrival_time, processing_time, job_size, job_id):
        self.arrivalTime = arrival_time
        self.processingTime = processing_time
        self.jobSize = job_size
        self.jobId = job_id


def main():
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()


if __name__ == '__main__':
    # start main
    main()
