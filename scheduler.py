"""
CPU Scheduling Algorithms Implementation
Implements various CPU scheduling algorithms for process management
"""

from typing import List, Tuple
from process import Process, ProcessState
import copy


class CPUScheduler:
    """Base class for CPU scheduling algorithms"""
    
    def __init__(self, processes: List[Process]):
        self.processes = [copy.deepcopy(p) for p in processes]
        self.current_time = 0
        self.gantt_chart = []
        self.completed_processes = []
    
    def schedule(self) -> Tuple[List[dict], dict, List[Tuple[int, int, str]]]:
        """
        Execute the scheduling algorithm
        Returns: (statistics, metrics, gantt_chart)
        """
        raise NotImplementedError("Subclass must implement schedule method")
    
    def calculate_metrics(self) -> dict:
        """Calculate average metrics for all processes"""
        n = len(self.completed_processes)
        if n == 0:
            return {}
        
        avg_turnaround = sum(p.turnaround_time for p in self.completed_processes) / n
        avg_waiting = sum(p.waiting_time for p in self.completed_processes) / n
        avg_response = sum(p.response_time for p in self.completed_processes) / n
        
        return {
            'avg_turnaround_time': round(avg_turnaround, 2),
            'avg_waiting_time': round(avg_waiting, 2),
            'avg_response_time': round(avg_response, 2),
            'total_processes': n
        }
    
    def get_results(self) -> Tuple[List[dict], dict, List[Tuple[int, int, str]]]:
        """Get scheduling results including process statistics and metrics"""
        stats = [p.get_statistics() for p in self.completed_processes]
        metrics = self.calculate_metrics()
        return stats, metrics, self.gantt_chart


class FCFSScheduler(CPUScheduler):
    """First Come First Serve (FCFS) Scheduling Algorithm"""
    
    def schedule(self):
        # Sort processes by arrival time
        self.processes.sort(key=lambda p: (p.arrival_time, p.pid))
        
        for process in self.processes:
            # Wait for process to arrive
            if self.current_time < process.arrival_time:
                self.gantt_chart.append((self.current_time, process.arrival_time, "IDLE"))
                self.current_time = process.arrival_time
            
            # Set process state and start time
            process.state = ProcessState.RUNNING
            process.start_time = self.current_time
            process.response_time = self.current_time - process.arrival_time
            
            # Execute process
            execution_time = process.burst_time
            self.gantt_chart.append((self.current_time, self.current_time + execution_time, f"P{process.pid}"))
            self.current_time += execution_time
            
            # Complete process
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.state = ProcessState.TERMINATED
            process.remaining_time = 0
            
            self.completed_processes.append(process)
        
        return self.get_results()


class SJFScheduler(CPUScheduler):
    """Shortest Job First (SJF) Non-Preemptive Scheduling Algorithm"""
    
    def schedule(self):
        ready_queue = []
        remaining_processes = self.processes.copy()
        remaining_processes.sort(key=lambda p: (p.arrival_time, p.pid))
        
        while remaining_processes or ready_queue:
            # Add arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival_time <= self.current_time:
                process = remaining_processes.pop(0)
                process.state = ProcessState.READY
                ready_queue.append(process)
            
            if not ready_queue:
                # CPU is idle
                if remaining_processes:
                    next_arrival = remaining_processes[0].arrival_time
                    self.gantt_chart.append((self.current_time, next_arrival, "IDLE"))
                    self.current_time = next_arrival
                continue
            
            # Select process with shortest burst time
            ready_queue.sort(key=lambda p: (p.burst_time, p.arrival_time, p.pid))
            process = ready_queue.pop(0)
            
            # Execute process
            process.state = ProcessState.RUNNING
            process.start_time = self.current_time
            process.response_time = self.current_time - process.arrival_time
            
            execution_time = process.burst_time
            self.gantt_chart.append((self.current_time, self.current_time + execution_time, f"P{process.pid}"))
            self.current_time += execution_time
            
            # Complete process
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.state = ProcessState.TERMINATED
            process.remaining_time = 0
            
            self.completed_processes.append(process)
        
        return self.get_results()


class SRTFScheduler(CPUScheduler):
    """Shortest Remaining Time First (SRTF) Preemptive Scheduling Algorithm"""
    
    def schedule(self):
        ready_queue = []
        remaining_processes = self.processes.copy()
        remaining_processes.sort(key=lambda p: (p.arrival_time, p.pid))
        current_process = None
        
        # Find the maximum completion time
        max_time = sum(p.burst_time for p in self.processes) + max(p.arrival_time for p in self.processes)
        
        for time in range(max_time + 1):
            self.current_time = time
            
            # Add newly arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival_time <= time:
                process = remaining_processes.pop(0)
                process.state = ProcessState.READY
                ready_queue.append(process)
            
            # Check if current process should be preempted
            if current_process:
                if current_process.is_complete():
                    current_process.completion_time = time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.completed_processes.append(current_process)
                    current_process = None
                elif ready_queue:
                    # Check for preemption
                    shortest = min(ready_queue, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
                    if shortest.remaining_time < current_process.remaining_time:
                        current_process.state = ProcessState.READY
                        ready_queue.append(current_process)
                        current_process = None
            
            # Select process with shortest remaining time
            if not current_process and ready_queue:
                ready_queue.sort(key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
                current_process = ready_queue.pop(0)
                current_process.state = ProcessState.RUNNING
                
                if current_process.start_time == -1:
                    current_process.start_time = time
                    current_process.response_time = time - current_process.arrival_time
            
            # Execute current process for 1 time unit
            if current_process:
                if not self.gantt_chart or self.gantt_chart[-1][2] != f"P{current_process.pid}":
                    self.gantt_chart.append([time, time + 1, f"P{current_process.pid}"])
                else:
                    self.gantt_chart[-1][1] = time + 1
                
                current_process.execute(1)
            else:
                # CPU is idle
                if not self.gantt_chart or self.gantt_chart[-1][2] != "IDLE":
                    self.gantt_chart.append([time, time + 1, "IDLE"])
                else:
                    self.gantt_chart[-1][1] = time + 1
            
            # Check if all processes are complete
            if not remaining_processes and not ready_queue and (not current_process or current_process.is_complete()):
                if current_process and current_process.is_complete():
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.completed_processes.append(current_process)
                break
        
        # Convert gantt chart lists to tuples
        self.gantt_chart = [(start, end, proc) for start, end, proc in self.gantt_chart]
        
        return self.get_results()


class RoundRobinScheduler(CPUScheduler):
    """Round Robin Scheduling Algorithm with Time Quantum"""
    
    def __init__(self, processes: List[Process], time_quantum: int = 2):
        super().__init__(processes)
        self.time_quantum = time_quantum
    
    def schedule(self):
        ready_queue = []
        remaining_processes = self.processes.copy()
        remaining_processes.sort(key=lambda p: (p.arrival_time, p.pid))
        
        while remaining_processes or ready_queue:
            # Add arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival_time <= self.current_time:
                process = remaining_processes.pop(0)
                process.state = ProcessState.READY
                ready_queue.append(process)
            
            if not ready_queue:
                # CPU is idle
                if remaining_processes:
                    next_arrival = remaining_processes[0].arrival_time
                    self.gantt_chart.append((self.current_time, next_arrival, "IDLE"))
                    self.current_time = next_arrival
                continue
            
            # Select first process from ready queue
            process = ready_queue.pop(0)
            process.state = ProcessState.RUNNING
            
            if process.start_time == -1:
                process.start_time = self.current_time
                process.response_time = self.current_time - process.arrival_time
            
            # Execute process for time quantum or remaining time
            execution_time = min(self.time_quantum, process.remaining_time)
            self.gantt_chart.append((self.current_time, self.current_time + execution_time, f"P{process.pid}"))
            
            process.execute(execution_time)
            self.current_time += execution_time
            
            # Add newly arrived processes during execution
            while remaining_processes and remaining_processes[0].arrival_time <= self.current_time:
                new_process = remaining_processes.pop(0)
                new_process.state = ProcessState.READY
                ready_queue.append(new_process)
            
            # Check if process is complete
            if process.is_complete():
                process.completion_time = self.current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                self.completed_processes.append(process)
            else:
                # Return to ready queue
                process.state = ProcessState.READY
                ready_queue.append(process)
        
        return self.get_results()


class PriorityScheduler(CPUScheduler):
    """Priority Scheduling Algorithm (Non-Preemptive)"""
    
    def schedule(self):
        ready_queue = []
        remaining_processes = self.processes.copy()
        remaining_processes.sort(key=lambda p: (p.arrival_time, p.pid))
        
        while remaining_processes or ready_queue:
            # Add arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival_time <= self.current_time:
                process = remaining_processes.pop(0)
                process.state = ProcessState.READY
                ready_queue.append(process)
            
            if not ready_queue:
                # CPU is idle
                if remaining_processes:
                    next_arrival = remaining_processes[0].arrival_time
                    self.gantt_chart.append((self.current_time, next_arrival, "IDLE"))
                    self.current_time = next_arrival
                continue
            
            # Select process with highest priority (lowest priority number)
            ready_queue.sort(key=lambda p: (p.priority, p.arrival_time, p.pid))
            process = ready_queue.pop(0)
            
            # Execute process
            process.state = ProcessState.RUNNING
            process.start_time = self.current_time
            process.response_time = self.current_time - process.arrival_time
            
            execution_time = process.burst_time
            self.gantt_chart.append((self.current_time, self.current_time + execution_time, f"P{process.pid}"))
            self.current_time += execution_time
            
            # Complete process
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.state = ProcessState.TERMINATED
            process.remaining_time = 0
            
            self.completed_processes.append(process)
        
        return self.get_results()
