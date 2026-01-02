#!/usr/bin/env python3
"""
Quick Start Guide for OS Lab Project
Run this script for a quick demonstration of the simulator
"""

from process import Process
from scheduler import FCFSScheduler, SJFScheduler, RoundRobinScheduler
from visualization import print_gantt_chart, print_statistics, compare_algorithms


def quick_demo():
    """Quick demonstration of CPU scheduling algorithms"""
    
    print("\n" + "="*90)
    print(" "*25 + "QUICK START DEMONSTRATION")
    print("="*90)
    
    # Create sample processes
    processes = [
        Process(1, 0, 4, priority=2),
        Process(2, 1, 3, priority=1),
        Process(3, 2, 1, priority=3),
        Process(4, 3, 5, priority=2),
    ]
    
    print("\nSample Processes:")
    print("-" * 90)
    for p in processes:
        print(f"  Process {p.pid}: Arrival={p.arrival_time}, Burst={p.burst_time}, Priority={p.priority}")
    
    print("\n" + "="*90)
    print("Running CPU Scheduling Algorithms...")
    print("="*90 + "\n")
    
    # Run algorithms
    results = {}
    
    # FCFS
    print("\n1. First Come First Serve (FCFS)")
    print("-" * 90)
    fcfs = FCFSScheduler(processes)
    stats, metrics, gantt = fcfs.schedule()
    print_gantt_chart(gantt, "FCFS")
    print(f"Average Turnaround Time: {metrics['avg_turnaround_time']}")
    print(f"Average Waiting Time:    {metrics['avg_waiting_time']}")
    results["FCFS"] = (stats, metrics)
    
    # SJF
    print("\n2. Shortest Job First (SJF)")
    print("-" * 90)
    sjf = SJFScheduler(processes)
    stats, metrics, gantt = sjf.schedule()
    print_gantt_chart(gantt, "SJF")
    print(f"Average Turnaround Time: {metrics['avg_turnaround_time']}")
    print(f"Average Waiting Time:    {metrics['avg_waiting_time']}")
    results["SJF"] = (stats, metrics)
    
    # Round Robin
    print("\n3. Round Robin (Time Quantum = 2)")
    print("-" * 90)
    rr = RoundRobinScheduler(processes, time_quantum=2)
    stats, metrics, gantt = rr.schedule()
    print_gantt_chart(gantt, "Round Robin")
    print(f"Average Turnaround Time: {metrics['avg_turnaround_time']}")
    print(f"Average Waiting Time:    {metrics['avg_waiting_time']}")
    results["Round Robin (Q=2)"] = (stats, metrics)
    
    # Comparison
    print("\n" + "="*90)
    compare_algorithms(results)
    
    print("\n" + "="*90)
    print("Quick Start Demo Complete!")
    print("="*90)
    print("\nNext Steps:")
    print("  1. Run 'python3 simulator.py' for interactive mode")
    print("  2. Run 'python3 simulator.py --demo' for complete demonstration")
    print("  3. Run 'python3 examples.py' for more examples")
    print("  4. Run 'python3 tests.py' to verify installation")
    print("="*90 + "\n")


if __name__ == "__main__":
    quick_demo()
