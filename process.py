"""
Process Class for CPU Scheduling Simulator
Represents a process with its attributes and state management
"""

from enum import Enum
from typing import Optional


class ProcessState(Enum):
    """Enum representing the different states of a process"""
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"


class Process:
    """
    Represents a process in the operating system simulator
    
    Attributes:
        pid: Process ID
        arrival_time: Time when process arrives in the system
        burst_time: CPU time required by the process
        priority: Priority of the process (lower number = higher priority)
        state: Current state of the process
        remaining_time: Remaining CPU time for the process
        completion_time: Time when process completes execution
        turnaround_time: Total time from arrival to completion
        waiting_time: Total time spent in ready queue
        response_time: Time from arrival to first execution
        start_time: Time when process first gets CPU
    """
    
    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int = 0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.state = ProcessState.NEW
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1
        self.start_time = -1
    
    def execute(self, time_slice: int = 1) -> int:
        """
        Execute the process for given time slice
        
        Args:
            time_slice: Amount of CPU time to execute
            
        Returns:
            Actual time executed
        """
        if self.state != ProcessState.RUNNING:
            return 0
        
        executed = min(time_slice, self.remaining_time)
        self.remaining_time -= executed
        
        if self.remaining_time == 0:
            self.state = ProcessState.TERMINATED
        
        return executed
    
    def is_complete(self) -> bool:
        """Check if process has completed execution"""
        return self.remaining_time == 0
    
    def __repr__(self):
        return (f"Process(PID={self.pid}, Arrival={self.arrival_time}, "
                f"Burst={self.burst_time}, Priority={self.priority}, "
                f"State={self.state.value})")
    
    def __str__(self):
        return f"P{self.pid}"
    
    def get_statistics(self) -> dict:
        """Get process statistics"""
        return {
            'pid': self.pid,
            'arrival_time': self.arrival_time,
            'burst_time': self.burst_time,
            'priority': self.priority,
            'completion_time': self.completion_time,
            'turnaround_time': self.turnaround_time,
            'waiting_time': self.waiting_time,
            'response_time': self.response_time
        }
