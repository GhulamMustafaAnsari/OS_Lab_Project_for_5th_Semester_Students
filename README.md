# OS Lab Project: Multi-Threaded Process Management & CPU Scheduling Simulator

A comprehensive Operating Systems lab project for 5th semester students that demonstrates various CPU scheduling algorithms and multi-threading concepts.

## 🎯 Project Overview

This project implements a complete CPU scheduling simulator with the following features:

### CPU Scheduling Algorithms
- **First Come First Serve (FCFS)** - Non-preemptive
- **Shortest Job First (SJF)** - Non-preemptive
- **Shortest Remaining Time First (SRTF)** - Preemptive
- **Round Robin (RR)** - Preemptive with configurable time quantum
- **Priority Scheduling** - Non-preemptive

### Multi-Threading Features
- Multi-threaded process execution simulation
- Process synchronization with mutex locks
- Semaphore demonstration
- Deadlock prevention techniques

### Visualization & Analysis
- Gantt charts for process execution timeline
- Detailed process statistics (Turnaround Time, Waiting Time, Response Time)
- Algorithm comparison and performance metrics
- Interactive command-line interface

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## 🚀 Quick Start

### Quick Demo (Recommended for First Time)

```bash
python3 quickstart.py
```

This runs a quick demonstration showing FCFS, SJF, and Round Robin algorithms with sample data.

### Running the Main Simulator

```bash
python3 simulator.py
```

This will launch an interactive menu with the following options:
1. Run All CPU Scheduling Algorithms (with sample data)
2. Run All CPU Scheduling Algorithms (with custom data)
3. Run Multi-Threaded Process Simulation
4. Run Process Synchronization Demonstration
5. Run Complete Demo (All Features)
6. Exit

### Running the Complete Demo

```bash
python3 simulator.py --demo
```

This will automatically run all features without user interaction.

### Running Examples

```bash
python3 examples.py
```

Demonstrates each scheduling algorithm with specific example cases.

### Running Tests

```bash
python3 tests.py
```

Runs the test suite to verify all algorithms work correctly.

## 📚 Project Structure

```
OS_Lab_Project_for_5th_Semester_Students/
│
├── process.py          # Process class and state management
├── scheduler.py        # CPU scheduling algorithm implementations
├── multithreading.py   # Multi-threading and synchronization demos
├── visualization.py    # Output formatting and visualization utilities
├── simulator.py        # Main interactive simulator
├── quickstart.py       # Quick demonstration script
├── examples.py         # Example use cases for each algorithm
├── tests.py           # Test suite for validation
├── requirements.txt   # Python dependencies (none required)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## 🔍 Detailed Features

### 1. Process Management

Each process has the following attributes:
- **PID**: Process ID
- **Arrival Time**: When the process arrives in the system
- **Burst Time**: CPU time required by the process
- **Priority**: Priority level (lower number = higher priority)
- **State**: Current state (NEW, READY, RUNNING, WAITING, TERMINATED)

### 2. CPU Scheduling Algorithms

#### First Come First Serve (FCFS)
- Executes processes in order of arrival
- Non-preemptive
- Simple but can cause convoy effect

#### Shortest Job First (SJF)
- Selects process with shortest burst time
- Non-preemptive
- Optimal for minimizing average waiting time

#### Shortest Remaining Time First (SRTF)
- Preemptive version of SJF
- Can interrupt running process for shorter job
- Better response time than SJF

#### Round Robin (RR)
- Each process gets fixed time quantum
- Preemptive and cyclic
- Fair allocation of CPU time

#### Priority Scheduling
- Executes processes based on priority
- Non-preemptive in this implementation
- Can be configured with different priority values

### 3. Performance Metrics

For each algorithm, the simulator calculates:

- **Completion Time**: When the process finishes execution
- **Turnaround Time**: Total time from arrival to completion
  - Formula: Completion Time - Arrival Time
- **Waiting Time**: Time spent waiting in ready queue
  - Formula: Turnaround Time - Burst Time
- **Response Time**: Time from arrival to first CPU allocation
  - Formula: Start Time - Arrival Time

### 4. Multi-Threading Features

#### Process Execution Simulation
- Simulates concurrent process execution using Python threads
- Demonstrates CPU multiplexing with configurable concurrency limit
- Real-time progress tracking

#### Synchronization Mechanisms
- **Mutex Locks**: Ensures mutual exclusion in critical sections
- **Semaphores**: Controls access to limited resources
- **Deadlock Prevention**: Demonstrates ordered resource acquisition

## 💡 Usage Examples

### Example 1: Compare All Algorithms

```python
from process import Process
from scheduler import FCFSScheduler, SJFScheduler, RoundRobinScheduler

processes = [
    Process(1, 0, 5, priority=2),
    Process(2, 1, 3, priority=1),
    Process(3, 2, 8, priority=3),
]

# FCFS
fcfs = FCFSScheduler(processes)
stats, metrics, gantt = fcfs.schedule()

# SJF
sjf = SJFScheduler(processes)
stats, metrics, gantt = sjf.schedule()

# Round Robin
rr = RoundRobinScheduler(processes, time_quantum=2)
stats, metrics, gantt = rr.schedule()
```

### Example 2: Custom Process Input

Run the simulator and select option 2 to enter custom process data:
- Arrival Time
- Burst Time
- Priority

### Example 3: Multi-Threading Demo

```python
from process import Process
from multithreading import MultiThreadedSimulator

processes = [
    Process(1, 0, 5, 0),
    Process(2, 1, 3, 0),
    Process(3, 2, 4, 0),
]

simulator = MultiThreadedSimulator(processes, max_concurrent=2)
execution_log, shared_data = simulator.simulate()
```

## 📊 Sample Output

### Gantt Chart Example
```
======================================================================
Gantt Chart - FCFS
======================================================================

| P1    | P2   | P3       | P4     | P5    |
0       5      8          16       22      26
```

### Statistics Table Example
```
==========================================================================================
Statistics - FCFS
==========================================================================================

PID    Arrival    Burst      Priority   Completion   TAT      WT       RT      
------------------------------------------------------------------------------------------
1      0          5          2          5            5        0        0       
2      1          3          1          8            7        4        4       
3      2          8          3          16           14       6        6       
4      3          6          2          22           19       13       13      
5      4          4          1          26           22       18       18      
------------------------------------------------------------------------------------------

Average Metrics
------------------------------------------------------------------------------------------
Average Turnaround Time: 13.4
Average Waiting Time:    8.2
Average Response Time:   8.2
Total Processes:         5
==========================================================================================
```

## 🎓 Educational Objectives

This project helps students understand:

1. **Process Scheduling**: How operating systems decide which process to run
2. **Algorithm Trade-offs**: Performance characteristics of different scheduling algorithms
3. **Multi-threading**: Concurrent execution and resource sharing
4. **Synchronization**: Preventing race conditions and deadlocks
5. **Performance Metrics**: Measuring and comparing system performance

## 🧪 Testing

The project includes a comprehensive test suite that validates:
- Process creation and state management
- Correctness of each scheduling algorithm
- Metrics calculation accuracy
- Edge cases and boundary conditions

Run tests with:
```bash
python3 tests.py
```

## 📝 Assignment Ideas

### Basic Level
1. Modify time quantum in Round Robin and observe effects
2. Add more processes and compare algorithm performance
3. Implement additional process states (BLOCKED, etc.)

### Intermediate Level
1. Implement Preemptive Priority Scheduling
2. Add aging mechanism to prevent starvation
3. Implement Multi-Level Queue Scheduling

### Advanced Level
1. Add I/O burst times and simulate I/O operations
2. Implement Multi-Level Feedback Queue (MLFQ)
3. Add memory management features
4. Implement process forking and parent-child relationships

## 🤝 Contributing

This is an educational project. Students are encouraged to:
- Add new scheduling algorithms
- Improve visualization
- Add more test cases
- Enhance documentation

## 📖 References

- Operating System Concepts by Silberschatz, Galvin, and Gagne
- Modern Operating Systems by Andrew S. Tanenbaum
- Operating Systems: Three Easy Pieces by Remzi H. Arpaci-Dusseau

## 📄 License

This project is created for educational purposes. Feel free to use and modify for learning.

## 👥 Credits

Created for 5th Semester Operating Systems Lab
Multi-Threaded Process Management & CPU Scheduling Simulator

---

**Note**: This is a simulation for educational purposes. Actual operating system schedulers are more complex and handle additional factors like I/O operations, interrupts, system calls, and hardware constraints.
