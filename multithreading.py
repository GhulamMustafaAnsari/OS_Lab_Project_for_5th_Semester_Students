"""
Multi-Threaded Process Simulator
Simulates process execution using multiple threads
"""

import threading
import time
from typing import List, Dict
from process import Process, ProcessState
import queue
import random


class ProcessThread(threading.Thread):
    """Thread that simulates a process execution"""
    
    def __init__(self, process: Process, shared_data: Dict, lock: threading.Lock):
        super().__init__()
        self.process = process
        self.shared_data = shared_data
        self.lock = lock
        self.daemon = True
    
    def run(self):
        """Execute the process simulation"""
        # Simulate process execution
        execution_units = self.process.burst_time
        
        for i in range(execution_units):
            with self.lock:
                if self.process.state == ProcessState.RUNNING:
                    # Simulate CPU work
                    time.sleep(0.1)  # Simulate 0.1 second per unit
                    self.process.remaining_time -= 1
                    
                    # Update shared data
                    if self.process.pid not in self.shared_data['progress']:
                        self.shared_data['progress'][self.process.pid] = 0
                    self.shared_data['progress'][self.process.pid] += 1
                    
                    if self.process.remaining_time == 0:
                        self.process.state = ProcessState.TERMINATED
                        self.shared_data['completed'].append(self.process.pid)


class MultiThreadedSimulator:
    """
    Multi-threaded process simulator that executes processes concurrently
    """
    
    def __init__(self, processes: List[Process], max_concurrent: int = 3):
        self.processes = processes
        self.max_concurrent = max_concurrent
        self.lock = threading.Lock()
        self.shared_data = {
            'progress': {},
            'completed': [],
            'current_time': 0
        }
    
    def simulate(self):
        """
        Simulate process execution with multiple threads
        Returns execution log and statistics
        """
        print(f"\n{'='*70}")
        print(f"Multi-Threaded Process Simulation")
        print(f"Maximum Concurrent Processes: {self.max_concurrent}")
        print(f"{'='*70}\n")
        
        execution_log = []
        active_threads = []
        process_queue = queue.Queue()
        
        # Sort processes by arrival time
        sorted_processes = sorted(self.processes, key=lambda p: p.arrival_time)
        for process in sorted_processes:
            process_queue.put(process)
        
        start_time = time.time()
        current_time = 0
        
        while not process_queue.empty() or active_threads:
            # Start new processes if slots available
            while len(active_threads) < self.max_concurrent and not process_queue.empty():
                process = process_queue.get()
                process.state = ProcessState.RUNNING
                
                thread = ProcessThread(process, self.shared_data, self.lock)
                thread.start()
                active_threads.append((thread, process))
                
                log_entry = f"[Time {current_time}] Process P{process.pid} started (Burst: {process.burst_time})"
                execution_log.append(log_entry)
                print(log_entry)
            
            # Check for completed threads
            completed = []
            for thread, process in active_threads:
                if not thread.is_alive() or process.state == ProcessState.TERMINATED:
                    if thread.is_alive():
                        thread.join(timeout=0.5)
                    completed.append((thread, process))
                    
                    log_entry = f"[Time {current_time}] Process P{process.pid} completed"
                    execution_log.append(log_entry)
                    print(log_entry)
            
            # Remove completed threads
            for item in completed:
                active_threads.remove(item)
            
            # Display progress
            if active_threads:
                progress_info = []
                for _, proc in active_threads:
                    done = self.shared_data['progress'].get(proc.pid, 0)
                    progress_info.append(f"P{proc.pid}({done}/{proc.burst_time})")
                
                log_entry = f"[Time {current_time}] Active: {', '.join(progress_info)}"
                print(log_entry)
            
            time.sleep(0.3)
            current_time += 1
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*70}")
        print(f"Simulation completed in {elapsed_time:.2f} seconds")
        print(f"Total processes completed: {len(self.shared_data['completed'])}")
        print(f"{'='*70}\n")
        
        return execution_log, self.shared_data


class SynchronizationDemo:
    """
    Demonstrates process synchronization with mutex locks and semaphores
    """
    
    def __init__(self):
        self.shared_resource = 0
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(2)  # Allow 2 threads at a time
        self.results = []
    
    def critical_section_with_lock(self, thread_id: int):
        """Demonstrate critical section with mutex lock"""
        for i in range(3):
            with self.lock:
                old_value = self.shared_resource
                time.sleep(0.01)  # Simulate work
                self.shared_resource = old_value + 1
                self.results.append(f"Thread {thread_id}: Resource = {self.shared_resource}")
    
    def critical_section_with_semaphore(self, thread_id: int):
        """Demonstrate critical section with semaphore"""
        with self.semaphore:
            self.results.append(f"Thread {thread_id} acquired semaphore")
            time.sleep(0.1)
            self.results.append(f"Thread {thread_id} released semaphore")
    
    def demonstrate_synchronization(self):
        """Run synchronization demonstration"""
        print(f"\n{'='*70}")
        print("Process Synchronization Demonstration")
        print(f"{'='*70}\n")
        
        # Mutex demonstration
        print("1. Mutex Lock Demonstration:")
        print("-" * 70)
        self.shared_resource = 0
        self.results = []
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=self.critical_section_with_lock, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        print(f"Final shared resource value: {self.shared_resource}")
        for result in self.results[-5:]:
            print(result)
        
        # Semaphore demonstration
        print(f"\n2. Semaphore Demonstration (max 2 concurrent):")
        print("-" * 70)
        self.results = []
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=self.critical_section_with_semaphore, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        for result in self.results:
            print(result)
        
        print(f"{'='*70}\n")


def demonstrate_deadlock_prevention():
    """Demonstrate deadlock prevention techniques"""
    print(f"\n{'='*70}")
    print("Deadlock Prevention Demonstration")
    print(f"{'='*70}\n")
    
    resource1 = threading.Lock()
    resource2 = threading.Lock()
    results = []
    
    def process1():
        # Ordered resource acquisition to prevent deadlock
        with resource1:
            results.append("Process 1: Acquired Resource 1")
            time.sleep(0.1)
            with resource2:
                results.append("Process 1: Acquired Resource 2")
                time.sleep(0.1)
                results.append("Process 1: Released both resources")
    
    def process2():
        # Same order as process1 to prevent deadlock
        with resource1:
            results.append("Process 2: Acquired Resource 1")
            time.sleep(0.1)
            with resource2:
                results.append("Process 2: Acquired Resource 2")
                time.sleep(0.1)
                results.append("Process 2: Released both resources")
    
    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("Ordered Resource Acquisition (Deadlock Prevention):")
    for result in results:
        print(f"  {result}")
    
    print(f"{'='*70}\n")
